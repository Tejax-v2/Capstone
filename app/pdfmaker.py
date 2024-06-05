from fpdf import FPDF
import datetime

def make_pdf(output,battery,memory):
    # Create instance of FPDF class
    pdf = FPDF(format=(200,250))

    pdf.set_author("Tejas Tupke")

    # Add a page
    pdf.add_page()

    # Set font
    pdf.set_font("Arial",style='B', size=30)

    # Define the text
    text = "Device Health Report"

    # Calculate width of the text in the selected font
    text_width = pdf.get_string_width(text)

    # Get the dimensions of the page
    page_width = pdf.w - 2 * pdf.l_margin  # Account for margins
    page_height = pdf.h - 2 * pdf.t_margin

    # Calculate x and y positions for the text to be centered
    x = (page_width - text_width) / 2 + pdf.l_margin
    y = page_height / 2 + pdf.t_margin

    # Set position and write the text
    pdf.set_xy(x, y)
    pdf.cell(text_width, 10, text)

    # Set font
    pdf.set_font("Arial", style='B', size=20)# Set font

    pdf.set_xy(10,10)
    pdf.cell(80, 10, txt=f"DoctorDroid", ln=True)

    # Set font
    pdf.set_font("Arial", size=12)

    pdf.set_xy(10,page_height-30)
    pdf.cell(80, 10, txt=f"IP Address - 127.0.0.1", ln=True)

    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")

    pdf.set_xy(10,page_height-20)
    pdf.cell(80, 10, txt=f"Date - {now}", ln=True)

    pdf.set_xy(10,page_height-10)
    pdf.cell(80, 10, txt="Developed by - Tejas Tupke", ln=True)


    # DEVICE HARDWARE INFORMATION
    pdf.add_page()
    pdf.set_font('Arial',style='B',size=16)

    pdf.cell(0, 10, txt="Device Hardware Information", ln=True, align='C')

    pdf.set_font('Arial',size=12)
    i=30
    for key,value in output.items():
        # device_info += f"{key}: {value}\n"
        if i > page_height-20:
            pdf.add_page()
            i=30
        pdf.set_xy(10,i)
        pdf.cell(70,10,txt=f"{key}")
        pdf.set_xy(80,i)
        pdf.cell(70,10,txt=f"{value}")
        i+=5
    

    # BATTERY STATISTICS

    pdf.add_page()
    pdf.set_font('Arial',style='B',size=16)

    pdf.cell(0,10, txt="Battery Statistics", ln=True, align='C')

    pdf.set_font('Arial',size=12)
    i=30
    for key,value in battery.items():
        if i > page_height-20:
            pdf.add_page()
            i=30
        pdf.set_xy(10,i)
        pdf.cell(70,10,txt=f"{key}")
        pdf.set_xy(80,i)
        pdf.cell(70,10,txt=f"{value}")
        i+=5
        
    # MEMORY STATISTICS

    pdf.add_page()
    pdf.set_font('Arial',style='B',size=16)

    pdf.cell(0,10, txt="Memory Snapshot", ln=True, align='C')

    pdf.set_font('Arial',size=12)
    i=30
    for key,value in memory.items():
        if i > page_height-20:
            pdf.add_page()
            i=30
        pdf.set_xy(10,i)
        pdf.cell(70,10,txt=f"{key}")
        pdf.set_xy(80,i)
        pdf.cell(70,10,txt=f"{value}")
        i+=5


    # Save the pdf with name .pdf
    pdf.output("report.pdf")
