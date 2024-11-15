import svgutils.transform as sg
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring
import os
from report_parser import ReportParser

def create_merged_svg(
    template_svg_path,
    company_name_text,
    type_text_value,
    citation_text,
    description_text,
    sankey_svg_path,
    center_description_text
):
    # Import the SVG template first to get its dimensions
    template = sg.fromfile(template_svg_path)
    template_root = template.getroot()
    
    # Get template dimensions
    try:
        template_width = float(template.width or 1500)
        template_height = float(template.height or 900)
    except (AttributeError, TypeError):
        template_width = 1500
        template_height = 900
    
    # Create figure with exact template dimensions
    figure = sg.SVGFigure()
    figure.set_size((str(template_width), str(template_height)))
    
    # Calculate text positions based on template width
    title_x = template_width * 0.05  # 5% from left
    title_y = template_height * 0.08  # 8% from top
    
    text_right_margin = template_width * 0.95  # 95% from left
    date_y = title_y  # Align with title vertically
    desc_y = date_y + 15  # 15 pixels below the source/citation
    
    # Create company name text element (bold)
    company_name = sg.TextElement(title_x, title_y, company_name_text,
                              size=24,
                              anchor='start')
    company_name.root.attrib['style'] = 'font-weight: bold'
    
    # Create type text element (not bold)
    type_text = sg.TextElement(title_x + len(company_name_text) * 18, title_y, type_text_value,
                              size=24,
                              anchor='start')
    
    # Create separate elements for "Source: " and the citation
    source_prefix = sg.TextElement(text_right_margin - len(citation_text)*6, date_y, "Source: ",
                                 size=10,
                                 anchor='end')
    
    citation_element = sg.TextElement(text_right_margin, date_y, citation_text,
                                    size=10,
                                    anchor='end')
    citation_element.root.attrib['style'] = 'text-decoration: underline'
    
    # Create description text element
    desc_svg = sg.TextElement(text_right_margin, desc_y, description_text,
                             size=10,
                             anchor='end')
    
    # Calculate position for centered description below Sankey
    center_desc_x = template_width / 2  # Center horizontally
    center_desc_y = template_height * 0.83  # Changed from 0.85 to 0.75 (moves it up)
    
    # Create centered description text element
    center_description = sg.TextElement(center_desc_x, center_desc_y, f'"{center_description_text}"',
                                      size=16,
                                      anchor='middle')
    # Add italic style to the underlying element
    center_description.root.attrib['style'] = 'font-style: italic'
    
    # Update elements list to include both text elements
    elements = [template_root, company_name, type_text, source_prefix, citation_element, desc_svg, center_description]
    
    # Import and add Sankey diagram if it exists
    if sankey_svg_path and os.path.exists(sankey_svg_path):
        try:
            sankey = sg.fromfile(sankey_svg_path)
            sankey_root = sankey.getroot()
            
            # Set Sankey dimensions to match template dimensions
            sankey_width = template_width
            sankey_height = template_height
            
            # Calculate position - horizontal center, slightly below vertical center
            x_center = (template_width - sankey_width) / 2  # Center horizontally
            y_center = ((template_height - sankey_height) / 2) + (template_height * 0.05)  # 5% below center
            
            # Create a group for the Sankey diagram
            sankey_group = sg.GroupElement([sankey_root])
            sankey_group.moveto(x_center, y_center)
            sankey_group.scale(1.0)
            
            elements.append(sankey_group)
            
        except Exception as e:
            print(f"Error loading Sankey SVG: {e}")
    
    figure.append(elements)
    return figure

def save_merged_svg(figure, output_path="merged_output.svg"):
    # Get the root and its dimensions
    root = figure.getroot()
    
    # Create the SVG string with proper XML headers and namespaces
    svg_str = f'''<?xml version="1.0" encoding="utf-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" 
         xmlns:xlink="http://www.w3.org/1999/xlink"
         width="{figure.width}" 
         height="{figure.height}"
         viewBox="0 0 {figure.width} {figure.height}">
    '''
    
    # Add the content of the figure
    for element in root:
        if hasattr(element, 'tostr'):  # svgutils elements
            svg_str += element.tostr().decode('utf-8')
        elif isinstance(element, (Element, str)):  # XML elements or strings
            svg_str += tostring(element).decode('utf-8')
    
    svg_str += '</svg>'
    
    # Write the complete SVG to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_str)
    
    print(f"SVG saved successfully to {output_path}")

def main(report_file_path=None, template_svg_path=None, sankey_svg_path=None):
    try:
        # Set default paths if not provided
        report_file_path = report_file_path or "/Users/thyag/Desktop/MonkTech/AAPL.txt"
        template_svg_path = template_svg_path or "/Users/thyag/Desktop/MonkTech/Template.svg"
        sankey_svg_path = sankey_svg_path or "/Users/thyag/Desktop/MonkTech/sankeymatic.svg"
        
        # Initialize the report parser
        parser = ReportParser()
        
        # Read the report text from file
        try:
            with open(report_file_path, 'r', encoding='utf-8') as file:
                report_text = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Report file not found at {report_file_path}")
        except Exception as e:
            raise Exception(f"Error reading report file: {e}")
        
        # Extract information from the report
        report_info = parser.extract_report_info(report_text)
        
        if not report_info:
            raise ValueError("Failed to parse report information")
        
        # Create merged SVG with extracted information
        merged_figure = create_merged_svg(
            template_svg_path=template_svg_path,
            sankey_svg_path=sankey_svg_path,
            **report_info
        )
        
        save_merged_svg(merged_figure)
        print("Merged SVG created successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    # You can call main() with specific paths if needed
    main()
