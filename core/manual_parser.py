import re
from pdfminer.high_level import extract_text  # Import the correct module

class ManualParser:
    def __init__(self, manual_path):
        """Initialize the parser with a file path."""
        self.manual_text = self._load_manual(manual_path)

    def _load_manual(self, manual_path):
        """Load manual text from a PDF or text file."""
        if manual_path.endswith(".pdf"):
            return extract_text(manual_path)  # Use pdfminer.high_level.extract_text
        else:
            with open(manual_path, "r", encoding="utf-8") as file:
                return file.read()

    def extract_fastener_guidelines(self):
        """Extract fastener types, sizes, materials, and applications from any manual structure."""
        fasteners = {}
        
        # Find all fastener sections dynamically
        fastener_sections = re.split(r"\n\s*\n", self.manual_text)  # Split by empty lines

        for section in fastener_sections:
            lines = section.strip().split("\n")

            # Identify a potential fastener type dynamically
            fastener_name_match = re.search(r"([A-Z][a-z]+ Head Screws)", section)
            if fastener_name_match:
                fastener_name = fastener_name_match.group(1).strip()
                fasteners[fastener_name] = {}

                # Extract Materials
                material_match = re.search(r"(?:Materials?|Common Finishes):\s*(.+)", section, re.IGNORECASE)
                if material_match:
                    fasteners[fastener_name]["materials"] = [m.strip() for m in material_match.group(1).split(",")]

                # Extract Standard Sizes (Finding size-related numbers)
                size_match = re.findall(r"(\d+\.?\d*\s*mm)", section)
                if size_match:
                    fasteners[fastener_name]["size_range"] = size_match

                # Extract Reason/Usage
                reason_match = re.search(r"(?:Used for|Applications?):\s*(.+)", section, re.IGNORECASE)
                if reason_match:
                    fasteners[fastener_name]["reason"] = reason_match.group(1).strip()
                else:
                    fasteners[fastener_name]["reason"] = "No specific reason found."

        return fasteners