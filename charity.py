from dataclasses import dataclass


@dataclass
class Charity:
    name: str
    phone: str
    website: str
    profileLink: str
    address: str
    ein: str

    def __init__(self, name: str, phone: str, website: str, profile_link: str, address: str, ein: str) -> None:
        self.name = name
        self.phone = phone
        self.website = website
        self.profileLink = profile_link
        self.address = address
        self.ein = ein

