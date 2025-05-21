import os
import comtypes.client


def pptx_to_pdf(input_folder):
    # Creating output folder path
    output_folder = os.path.join(input_folder, "pdfs")
    os.makedirs(output_folder, exist_ok=True)

    # will start the PowerPoint app and run in background (make sure powerpoint isn't already open)
    powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
    powerpoint.Visible = 1

    for filename in os.listdir(input_folder):
        if filename.endswith(".pptx"):
            full_path = os.path.join(input_folder, filename)
            pdf_path = os.path.join(
                output_folder, os.path.splitext(filename)[0] + ".pdf")

            presentation = powerpoint.Presentations.Open(
                full_path, WithWindow=False)
            presentation.SaveAs(pdf_path, FileFormat=32)  # 32 = PDF
            presentation.Close()

    powerpoint.Quit()


ppt_folder = r"C:\Users\hp\Desktop\sem8\genAI\Slides"
pptx_to_pdf(ppt_folder)
