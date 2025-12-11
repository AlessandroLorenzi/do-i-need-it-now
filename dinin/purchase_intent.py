import uuid
from datetime import datetime, timedelta, timezone

from flask import Flask, render_template, request
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from db import db

app = Flask(__name__)


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
