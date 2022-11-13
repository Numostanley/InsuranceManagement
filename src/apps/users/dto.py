import dataclasses


@dataclasses.dataclass(init=False)
class RegisterUser:
    email: str
    first_name: str
    last_name: str
    phone_number: str
    username: str
    location: str
    password: str
    confirm_password: str
    group: str


@dataclasses.dataclass(init=False)
class UpdateUser:
    first_name: str
    last_name: str
    phone_number: str
    location: str
