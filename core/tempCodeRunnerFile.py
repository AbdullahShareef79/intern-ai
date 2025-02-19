class FastenerAgent:
    def __init__(self, guideline):
        """Initialize the fastener agent with structured guidelines."""
        self.guideline = guideline

    def _parse_length(self, length_str):
        """Parse a length range string (e.g., '20-100 mm') into min and max values."""
        try:
            # Handle different formats: "20-100 mm", "8mm-50mm", "15-120"
            clean_str = length_str.lower().replace('mm', '').strip()
            parts = clean_str.split('-')
            if len(parts) != 2:
                return None, None
            return float(parts[0].strip()), float(parts[1].strip())
        except (ValueError, AttributeError):
            return None, None

    def _match_fastener(self, fastener_type, features):
        """Check if features match a specific fastener type's requirements."""
        specs = self.guideline.get(fastener_type, {})
        reason = specs.get("reason", "")

        # Get critical features
        hole_depth = features.get('hole_depth', 0)
        geometry_type = features.get('geometry_type', '').lower()

        # Standardized geometry names
        flat_variants = ["flat", "planar", "smooth"]
        rounded_variants = ["rounded", "curved", "circular"]

        # Geometry compatibility check
        geometry_match = False
        if fastener_type == "Flat Head Screws":
            geometry_match = any(variant in geometry_type for variant in flat_variants)
        elif fastener_type == "Rounded Head Screws":
            geometry_match = any(variant in geometry_type for variant in rounded_variants)
        else:  # Hex & Socket Head Screws → No geometry dependency
            geometry_match = True

        if not geometry_match:
            return False, reason

        # Dimensional requirements check
        size_requirements = {
            "Hex Head Screws": "length_range",
            "Socket Head Screws": "thread_length",
            "Flat Head Screws": "length_range",
            "Rounded Head Screws": None  # No size check needed
        }

        req_field = size_requirements[fastener_type]
        if not req_field:
            return True, reason  # Rounded heads only need geometry match

        tolerance = 0.1  # Allow ±10% flexibility in depth matching

        for size_info in specs.get("sizes", []):
            length_str = size_info.get(req_field)
            if not length_str:
                continue
                        
            min_len, max_len = self._parse_length(length_str)
            if min_len and max_len and (min_len * (1 - tolerance)) <= hole_depth <= (max_len * (1 + tolerance)):
                return True, reason


        return False, reason

    def find_best_fastener(self, features):
        """Find the best fastener type based on extracted features."""
        try:
            print("\n🔍 Debug: Extracted Features for Fastener Selection")
            print(features)  # ✅ Print extracted features

            priority_order = [
                "Hex Head Screws",   
                "Socket Head Screws",  
                "Flat Head Screws",    
                "Rounded Head Screws"  
            ]

            for fastener_type in priority_order:
                matches, reason = self._match_fastener(fastener_type, features)
                if matches:
                    return {
                        "fastener_type": fastener_type,
                        "explanation": reason
                    }

            return {
                "fastener_type": "Socket Head Screws",
                "explanation": "Ideal for situations with limited space or where a clean, flush fit is needed. Commonly used in precision equipment"
            }

        except Exception as e:
            return {
                "fastener_type": "error",
                "explanation": f"Selection error: {str(e)}"
            }
