import base64
import io
import zipfile
import xml.etree.ElementTree as ET


def process_profile(profile_b64: str) -> str:
    """
    Traite le profile :
    - Décodage du fichier DOCX (archive ZIP) encodé en base64.
    - Extraction du document XML (word/document.xml).
    - Utilisation du fichier word/styles.xml pour appliquer la mise en forme du texte (titres).

    :param profile_b64: Chaîne base64 représentant le document DOCX.
    :return: Texte structuré extrait du document.
    """
    profile_bytes = base64.b64decode(profile_b64)
    zip_file = zipfile.ZipFile(io.BytesIO(profile_bytes))

    document_path = "word/document.xml"
    styles_path = "word/styles.xml"
    result_lines = []
    style_map = {}

    # Construction de la carte des styles
    if styles_path in zip_file.namelist():
        styles_xml = zip_file.read(styles_path)
        styles_tree = ET.fromstring(styles_xml)
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        for style in styles_tree.findall(".//w:style", ns):
            style_id = style.attrib.get(f"{{{ns['w']}}}styleId")
            name_elem = style.find("w:name", ns)
            if name_elem is not None:
                style_name = name_elem.attrib.get(f"{{{ns['w']}}}val", "")
                style_map[style_id] = style_name

    # Extraction du document principal
    if document_path in zip_file.namelist():
        document_xml = zip_file.read(document_path)
        tree = ET.fromstring(document_xml)
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        for para in tree.findall(".//w:p", ns):
            texts = [node.text for node in para.findall(".//w:t", ns) if node.text]
            if not texts:
                continue
            full_text = " ".join(texts).strip()
            p_style = para.find(".//w:pStyle", ns)
            if p_style is not None:
                style_id = p_style.attrib.get(f"{{{ns['w']}}}val")
                style_name = style_map.get(style_id, "")
                if "Heading1" in style_name:
                    result_lines.append(f"\n# {full_text}\n")
                elif "Heading2" in style_name:
                    result_lines.append(f"\n## {full_text}\n")
                elif "Heading3" in style_name:
                    result_lines.append(f"\n### {full_text}\n")
                else:
                    result_lines.append(full_text)
            else:
                result_lines.append(full_text)
    else:
        result_lines.append("Fichier 'word/document.xml' introuvable dans le profile.")

    return "\n".join(result_lines)