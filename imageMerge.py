import svgutils.transform as sg
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring
import os

def create_merged_svg(
    template_svg_path,
    title, 
    date_text, 
    description_text, 
    sankey_svg_path
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
    
    date_x = template_width * 0.95  # 95% from left
    date_y = title_y  # Align with title vertically
    
    desc_y = date_y + 30  # 30px below date
    
    # Create text elements with adjusted positions
    title_svg = sg.TextElement(title_x, title_y, title,
                             size=28,
                             weight="normal", 
                             font="Arial")
    
    date_svg = sg.TextElement(date_x, date_y, date_text,
                             size=16,
                             anchor='end', 
                             font="Arial", 
                             color="#666666")
    
    desc_svg = sg.TextElement(date_x, desc_y, description_text,
                             size=16,
                             anchor='end', 
                             font="Arial", 
                             color="#666666")
    
    # Add elements to figure
    elements = [template_root, title_svg, date_svg, desc_svg]
    
    # Import and add Sankey diagram if it exists
    if sankey_svg_path and os.path.exists(sankey_svg_path):
        try:
            sankey = sg.fromfile(sankey_svg_path)
            sankey_root = sankey.getroot()
            
            # Try to get Sankey dimensions
            try:
                sankey_width = float(sankey.width or 1000)
                sankey_height = float(sankey.height or 600)
            except (AttributeError, TypeError, ValueError):
                sankey_width = 1000
                sankey_height = 600
            
            # Calculate scale factor to fit within template
            available_width = template_width * 0.9  # Use 90% of template width
            scale_factor = min(0.8, available_width / sankey_width)
            
            # Center position
            x_center = (template_width - (sankey_width * scale_factor)) / 2
            y_position = template_height * 0.15  # 15% from top
            
            # Create a group for the Sankey diagram
            sankey_group = sg.GroupElement([sankey_root])
            sankey_group.moveto(x_center, y_position)
            sankey_group.scale(scale_factor)
            
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

def main():
    try:
        # Example usage
        merged_figure = create_merged_svg(
            template_svg_path="/Users/thyag/Desktop/MonkTech/Template.svg",
            title="Monthly Budget Analysis",
            date_text="November 10, 2024",
            description_text="Distribution of Monthly Income and Expenses",
            sankey_svg_path="/Users/thyag/Desktop/MonkTech/sankeymatic.svg"
        )
        
        save_merged_svg(merged_figure)
        print("Merged SVG created successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    main()