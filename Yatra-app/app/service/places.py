from models import PlacesResponseModel
from service.cache import get_cache, set_cache

# Mock places dataset keyed by lowercased destination.
# Entry fees are in GBP. None means free admission.
PLACES_DATABASE: dict[str, list[PlacesResponseModel]] = {
    "london": [
        PlacesResponseModel(
            name="British Museum",
            description="Eight million works of world history, from the Rosetta Stone to the Parthenon sculptures.",
            category="museum",
            rating=4.7,
            esttimated_time_hours="3-4",
            entry_fee=None
        ),
        PlacesResponseModel(
            name="Tower of London",
            description="Norman fortress on the Thames holding the Crown Jewels, with Yeoman Warder tours.",
            category="historical",
            rating=4.6,
            esttimated_time_hours="3",
            entry_fee=34.80
        ),
        PlacesResponseModel(
            name="National Gallery",
            description="Western European painting from the 13th to 19th century on Trafalgar Square.",
            category="art",
            rating=4.7,
            esttimated_time_hours="2-3",
            entry_fee=None
        ),
        PlacesResponseModel(
            name="Tate Modern",
            description="Modern and contemporary art in a converted Bankside power station on the South Bank.",
            category="art",
            rating=4.5,
            esttimated_time_hours="2-3",
            entry_fee=None
        ),
        PlacesResponseModel(
            name="Westminster Abbey",
            description="Gothic abbey that has hosted coronations since 1066, with Poets' Corner and royal tombs.",
            category="religious",
            rating=4.6,
            esttimated_time_hours="2",
            entry_fee=29.00
        ),
        PlacesResponseModel(
            name="Borough Market",
            description="Southwark food market trading since the 12th century; produce, cheese stalls and street food.",
            category="market",
            rating=4.4,
            esttimated_time_hours="1-2",
            entry_fee=None
        ),
        PlacesResponseModel(
            name="Hyde Park",
            description="350 acres of central parkland with the Serpentine lake, rowing boats and Speakers' Corner.",
            category="nature",
            rating=4.6,
            esttimated_time_hours="1-2",
            entry_fee=None
        ),
        PlacesResponseModel(
            name="Natural History Museum",
            description="Dinosaur galleries, the blue whale skeleton and mineral collections in a Romanesque hall.",
            category="museum",
            rating=4.7,
            esttimated_time_hours="3",
            entry_fee=None
        ),
        PlacesResponseModel(
            name="The London Eye",
            description="135 metre observation wheel on the South Bank; a full rotation takes about thirty minutes.",
            category="viewpoint",
            rating=4.3,
            esttimated_time_hours="1",
            entry_fee=32.50
        ),
        PlacesResponseModel(
            name="Camden Market",
            description="Canalside stalls for vintage clothing, records and international street food in north London.",
            category="market",
            rating=4.2,
            esttimated_time_hours="2-3",
            entry_fee=None
        ),
    ],
    "edinburgh": [
        PlacesResponseModel(
            name="Edinburgh Castle",
            description="Fortress on Castle Rock above the Old Town, home to the Honours of Scotland.",
            category="historical",
            rating=4.5,
            esttimated_time_hours="2-3",
            entry_fee=21.50
        ),
        PlacesResponseModel(
            name="Arthur's Seat",
            description="Extinct volcano in Holyrood Park with a short climb to views across the Firth of Forth.",
            category="nature",
            rating=4.8,
            esttimated_time_hours="2-3",
            entry_fee=None
        ),
        PlacesResponseModel(
            name="Royal Mile",
            description="The Old Town spine running from the castle to Holyrood, lined with closes and pubs.",
            category="historical",
            rating=4.5,
            esttimated_time_hours="2",
            entry_fee=None
        ),
        PlacesResponseModel(
            name="National Museum of Scotland",
            description="Scottish history, natural science and design under a Victorian glass-roofed atrium.",
            category="museum",
            rating=4.7,
            esttimated_time_hours="3",
            entry_fee=None
        ),
    ],
    "bath": [
        PlacesResponseModel(
            name="Roman Baths",
            description="Preserved bathing complex around a natural hot spring, with the Georgian Pump Room above.",
            category="historical",
            rating=4.6,
            esttimated_time_hours="2",
            entry_fee=28.00
        ),
        PlacesResponseModel(
            name="Royal Crescent",
            description="Palladian terrace of thirty houses curving above a lawn; No. 1 is a period museum.",
            category="historical",
            rating=4.6,
            esttimated_time_hours="1",
            entry_fee=15.00
        ),
        PlacesResponseModel(
            name="Bath Abbey",
            description="Perpendicular Gothic abbey with fan vaulting and a tower tour over the city.",
            category="religious",
            rating=4.5,
            esttimated_time_hours="1",
            entry_fee=7.50
        ),
    ],
    "manchester": [
        PlacesResponseModel(
            name="Science and Industry Museum",
            description="Mill engines, textile machinery and the world's oldest surviving passenger railway station.",
            category="museum",
            rating=4.5,
            esttimated_time_hours="2-3",
            entry_fee=None
        ),
        PlacesResponseModel(
            name="Old Trafford",
            description="Manchester United's stadium, with a museum and behind-the-scenes tour of the dressing rooms.",
            category="sports",
            rating=4.6,
            esttimated_time_hours="2",
            entry_fee=28.00
        ),
        PlacesResponseModel(
            name="Manchester Art Gallery",
            description="Pre-Raphaelite paintings, Victorian decorative art and contemporary shows on Mosley Street.",
            category="art",
            rating=4.4,
            esttimated_time_hours="1-2",
            entry_fee=None
        ),
        PlacesResponseModel(
            name="John Rylands Library",
            description="Neo-Gothic reading room in Deansgate holding early printed books and medieval manuscripts.",
            category="historical",
            rating=4.7,
            esttimated_time_hours="1",
            entry_fee=None
        ),
        PlacesResponseModel(
            name="Northern Quarter",
            description="Independent record shops, vintage stores and street art across the city's old textile district.",
            category="market",
            rating=4.3,
            esttimated_time_hours="2-3",
            entry_fee=None
        ),
    ],
}


async def fetch_places(destination: str) -> list[PlacesResponseModel]:
    """Return the top places to visit for a destination.

    Returns an empty list if the destination is not in the dataset.
    """
    places = list(PLACES_DATABASE.get(destination.strip().lower(), []))
    return places
