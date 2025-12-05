#!/usr/bin/env python3
import os
import uuid
from datetime import datetime, timedelta, timezone

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from mail_sender import MailSender
from open_graph_info_fetcher import OpenGraphInfoFetcher
from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = Flask(__name__)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


@app.route("/", methods=["GET"])
def index():
    email = request.cookies.get("email", "")
    return render_template("index.html", email=email)


class PurchaseIntent(db.Model):
    __tablename__ = "purchase_intent"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    notify_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc) + timedelta(days=7),
    )
    description: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)

    alternative: Mapped[str] = mapped_column(String, nullable=False)
    need_description: Mapped[str] = mapped_column(String, nullable=False)
    vanity_free_desire: Mapped[str] = mapped_column(String, nullable=False)
    notified: Mapped[bool] = mapped_column(default=False)


@app.route("/purchase-intent/submit", methods=["POST"])
def submit_purchase_intent():
    data = request.form.to_dict()
    # Check if a purchase intent already exists with the same email and url
    purchase_intent = PurchaseIntent.query.filter_by(
        email=data.get("email", ""), url=data.get("url", "")
    ).first()

    if not purchase_intent:
        purchase_intent = PurchaseIntent(
            description=data.get("description", ""),
            email=data.get("email", ""),
            url=data.get("url", ""),
            alternative=data.get("alternative", ""),
            need_description=data.get("need_description", ""),
            vanity_free_desire=data.get("vanity_free_desire", ""),
        )
        db.session.add(purchase_intent)
        db.session.commit()
    og_info = app.fetch_og.fetch(purchase_intent.url)

    response = render_template(
        "purchase_intent_submitted.html",
        purchase_intent=purchase_intent,
        og_info=og_info,
    )
    response = app.make_response(response)
    response.set_cookie("email", purchase_intent.email)
    return response


@app.route("/health", methods=["GET"])
def health_check():
    return "OK", 200


@app.route("/send-emails", methods=["GET"])
def send_emails():
    items_to_notify = (
        PurchaseIntent.query.filter_by(notified=False)
        # .filter(PurchaseIntent.notify_date <= datetime.now(timezone.utc))
        .all()
    )
    for item in items_to_notify:
        og_info = app.fetch_og.fetch(item.url)
        app.mail_sender.send_email(
            receiver_email=item.email,
            subject="[Do I Need It Now?] É il momento di rivalutare il tuo acquisto",
            text_body=render_template(
                "purchase_intent_email.txt", purchase_intent=item, og_info=og_info
            ),
            html_body=render_template(
                "purchase_intent_email.html", purchase_intent=item, og_info=og_info
            ),
        )
        item.notified = True
        db.session.commit()

    return f"Found {len(items_to_notify)} items to notify.", 200


if __name__ == "__main__":
    fetch_og = OpenGraphInfoFetcher()
    mail_sender = MailSender(
        smtp_server=os.getenv("SMTP_SERVER"),
        smtp_port=int(os.getenv("SMTP_PORT", 587)),
        sender_email=os.getenv("SENDER_EMAIL"),
        smtp_username=os.getenv("SMTP_USERNAME"),
        smtp_password=os.getenv("SMTP_PASSWORD"),
    )

    with app.app_context():
        db.create_all()
        app.fetch_og = fetch_og
        app.mail_sender = mail_sender
    with app.app_context():
        db.create_all()
    app.run(debug=True)
