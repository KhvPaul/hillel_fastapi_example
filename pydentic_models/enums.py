import enum


class Genders(str, enum.Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"


class UserRoles(str, enum.Enum):
    Admin = "Admin"
    Seller = "Seller"
    Customer = "Customer"
