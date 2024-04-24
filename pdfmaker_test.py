#***************************************************TEST CODE*************************************************

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Create a PdfPages object to save plots into a PDF file
with PdfPages('plots.pdf') as pdf:
    # Plot 1
    plt.figure()
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    plt.title('Plot 1')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    # Save the plot to the PDF file
    pdf.savefig()
    plt.close()

    # Plot 2
    plt.figure()
    plt.plot([1, 2, 3, 4], [1, 2, 3, 4])
    plt.title('Plot 2')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    # Save the plot to the PDF file
    pdf.savefig()
    plt.close()

    # Plot 3
    plt.figure()
    plt.plot([1, 2, 3, 4], [4, 3, 2, 1])
    plt.title('Plot 3')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    # Save the plot to the PDF file
    pdf.savefig()
    plt.close()

print("Plots saved to plots.pdf")
