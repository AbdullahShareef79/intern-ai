class FastenerGuideline:
    def __init__(self):
        """Structured fastener guidelines for quick lookup."""
        self.guidelines = {
            "Hex Head Screws": {
                "description": "Suitable for projects where strength and durability are crucial, such as heavy machinery or automotive applications.",
                "materials": ["stainless steel", "alloy steel"],
                "sizes": [
                    {"size": "M6", "thread_pitch": "1.0 mm", "length_range": "20-100 mm", "tensile_strength": "800-1000 MPa"},
                    {"size": "M8", "thread_pitch": "1.25 mm", "length_range": "25-120 mm", "tensile_strength": "800-1000 MPa"},
                    {"size": "M10", "thread_pitch": "1.5 mm", "length_range": "30-150 mm", "tensile_strength": "800-1000 MPa"}
                ],
                "standards": {
                    "ISO": "ISO 898-1",
                    "DIN": "DIN 933"
                },
                "reason": "Used for high-strength applications due to durability and high tensile strength."
            },
            "Socket Head Screws": {
                "description": "Ideal for situations with limited space or where a clean, flush fit is needed. Commonly used in precision equipment.",
                "materials": ["stainless steel", "black oxide"],
                "sizes": [
                    {"size": "M3", "head_diameter": "5.5 mm", "head_height": "3.0 mm", "thread_length": "8-50 mm"},
                    {"size": "M5", "head_diameter": "8.5 mm", "head_height": "5.0 mm", "thread_length": "10-60 mm"},
                    {"size": "M8", "head_diameter": "13.0 mm", "head_height": "8.0 mm", "thread_length": "15-80 mm"}
                ],
                "standards": {
                    "ISO": "ISO 4762",
                    "ANSI": "ASME B18.3"
                },
                "reason": "Ideal for tight spaces where a flush, clean fit is required."
            },
            "Rounded Head Screws": {
                "description": "Work best in decorative or low-profile designs, where appearance is important, such as furniture or consumer electronics.",
                "materials": ["brass", "chrome-plated", "zinc", "nickel-plated"],
                "sizes": [
                    {"size": "M2", "head_diameter": "4.0 mm", "head_height": "1.6 mm", "finishes": ["brass", "chrome-plated"]},
                    {"size": "M4", "head_diameter": "6.0 mm", "head_height": "2.5 mm", "finishes": ["zinc", "nickel-plated"]},
                    {"size": "M6", "head_diameter": "8.0 mm", "head_height": "3.5 mm", "finishes": ["stainless steel", "brass"]}
                ],
                "standards": {
                    "ISO": "ISO 7380"
                },
                "reason": "Best for decorative or low-profile designs where appearance is important."
            },
            "Flat Head Screws": {
                "description": "Recommended for situations where the screw must sit flush with the surface. Perfect for countersunk applications, such as cabinetry or structural panels.",
                "materials": ["stainless steel", "brass"],
                "sizes": [
                    {"size": "M4", "head_diameter": "7.5 mm", "countersink_angle": "90°", "length_range": "8-50 mm"},
                    {"size": "M6", "head_diameter": "11.0 mm", "countersink_angle": "90°", "length_range": "10-80 mm"},
                    {"size": "M8", "head_diameter": "14.5 mm", "countersink_angle": "90°", "length_range": "15-120 mm"}
                ],
                "standards": {
                    "ISO": "ISO 10642",
                    "ANSI": "ASME B18.3.6",
                    "DIN": "DIN 7991"
                },
                "reason": "Recommended for flush, countersunk applications."
            }
        }

    def get_guideline(self):
        """
        Return the full fastener guidelines dictionary.
        
        Returns:
            dict: Structured fastener guidelines.
        """
        return self.guidelines

    def get_fastener_info(self, fastener_type):
        """
        Get detailed information about a specific fastener type.
        
        Args:
            fastener_type (str): The type of fastener (e.g., "Hex Head Screws").
        
        Returns:
            dict: Information about the specified fastener type, or None if not found.
        """
        return self.guidelines.get(fastener_type, None)