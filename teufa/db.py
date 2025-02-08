from datetime import datetime

from authlib.integrations.sqla_oauth2 import (
    OAuth2AuthorizationCodeMixin,
    OAuth2ClientMixin,
    OAuth2TokenMixin,
)
from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    hostname: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    users: Mapped[list["User"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan"
    )
    airlines: Mapped[list["Airline"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan"
    )
    airports: Mapped[list["Airport"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan"
    )
    fleet: Mapped[list["Aircraft"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan"
    )
    liveries: Mapped[list["Livery"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan"
    )
    flights: Mapped[list["Flight"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan"
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"))
    name: Mapped[str]
    email: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    tenant: Mapped["Tenant"] = relationship(back_populates="users")
    oauth2_tokens: Mapped[list["OAuth2Token"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    oauth2_authorization_codes: Mapped[list["OAuth2AuthorizationCode"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def get_user_id(self):
        return self.id


class OAuth2Client(Base, OAuth2ClientMixin):
    __tablename__ = "oauth2_clients"

    id: Mapped[int] = mapped_column(primary_key=True)


class OAuth2Token(Base, OAuth2TokenMixin):
    __tablename__ = "oauth2_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="oauth2_tokens")


class OAuth2AuthorizationCode(Base, OAuth2AuthorizationCodeMixin):
    __tablename__ = "oauth2_authorization_codes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="oauth2_authorization_codes")


class Airline(Base):
    __tablename__ = "airlines"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"))
    name: Mapped[str]
    iata: Mapped[str]
    icao: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    tenant: Mapped["Tenant"] = relationship(back_populates="airlines")


class Airport(Base):
    __tablename__ = "airports"

    icao: Mapped[str] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"))
    iata: Mapped[str]
    name: Mapped[str]
    city: Mapped[str]
    country: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    tenant: Mapped["Tenant"] = relationship(back_populates="airports")


class Aircraft(Base):
    __tablename__ = "aircraft"
    __table_args__ = (UniqueConstraint("icao", "tail_number"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"))
    icao: Mapped[str]
    tail_number: Mapped[str | None]
    range_nm: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    tenant: Mapped["Tenant"] = relationship(back_populates="fleet")
    liveries: Mapped[list["Livery"]] = relationship(back_populates="aircraft")
    flights: Mapped[list["Flight"]] = relationship(back_populates="aircraft")


class Livery(Base):
    __tablename__ = "livery"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"))
    name: Mapped[str]
    aircraft_id: Mapped[int] = mapped_column(ForeignKey("aircraft.id"))
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    tenant: Mapped["Tenant"] = relationship(back_populates="liveries")
    aircraft: Mapped["Aircraft"] = relationship(back_populates="liveries")


class Flight(Base):
    __tablename__ = "flights"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"))
    departure_icao: Mapped[str]
    arrival_icao: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    aircraft_id: Mapped["Aircraft"] = mapped_column(ForeignKey("aircraft.id"))

    tenant: Mapped["Tenant"] = relationship(back_populates="flights")
    aircraft: Mapped["Aircraft"] = relationship(back_populates="flights")
