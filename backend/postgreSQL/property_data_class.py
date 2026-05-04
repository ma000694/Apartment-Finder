# data class used to insert properties with correct fields

from dataclasses import dataclass

@dataclass
class Property: # stored model
    building_name: str
    unit_name: str
    address: str
    beds: int
    baths: int
    rent: int
    sqft: int
    availability: str
    url: str
    amenities: str
    
    def __init__(self):
        self.building_name = "N/A"
        self.unit_name = "N/A"
        self.address = "N/A"
        self.beds = -1
        self.baths = -1
        self.rent = -1
        self.sqft = -1
        self.availability = "N/A"
        self.url = "N/A"
        self.amenities = "N/A"