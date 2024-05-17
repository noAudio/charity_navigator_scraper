from dataclasses import dataclass


@dataclass
class Charity:
    name: str
    phone: str
    website: str
    profileLink: str
    serviceArea: str

    def __init__(self, name: str, phone: str, website: str, profile_link: str, service_area: str) -> None:
        self.name = name
        self.phone = phone
        self.website = website
        self.profileLink = profile_link
        self.serviceArea = service_area
