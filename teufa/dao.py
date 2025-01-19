from pydantic import BaseModel

empty = object()


class Error(BaseModel):
    message: str


class Tenant(BaseModel):
    id: int | None = None
    name: str
    hostname: str


class PartialTenant(BaseModel):
    id: int | object = empty
    name: str | object = empty
    hostname: str | object = empty


class CreateTenantRequest(BaseModel):
    tenant: Tenant


class CreateTenantResponse(BaseModel):
    tenant: Tenant


class UpdateTenantRequest(BaseModel):
    tenant: PartialTenant


class UpdateTenantResponse(BaseModel):
    tenant: Tenant


class GetTenantResponse(BaseModel):
    tenant: Tenant


class Flight(BaseModel):
    id: int | None = None
    departure_icao: str
    arrival_icao: str
    aircraft_id: int


class PartialFlight(BaseModel):
    id: int | object = empty
    departure_icao: str | object = empty
    arrival_icao: str | object = empty
    aircraft_id: int | object = empty


class CreateFlightRequest(BaseModel):
    flight: Flight


class CreateFlightResponse(BaseModel):
    flight: Flight


class UpdateFlightRequest(BaseModel):
    flight: PartialFlight


class UpdateFlightResponse(BaseModel):
    flight: Flight


class GetFlightResponse(BaseModel):
    flight: Flight
