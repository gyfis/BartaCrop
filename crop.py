from PyPDF2 import PdfFileWriter, PdfFileReader
import argparse

__author__ = 'Gyfis'


if __name__ == '__main__':

    default_order = [1, 2, 3, 4]

    parser = argparse.ArgumentParser(description="Easily crop slides from your favorite teacher - BartaK!")
    parser.add_argument('input', nargs='*', default=[], help='The files you want to convert.')
    parser.add_argument('-m', '--margin', dest='margin', nargs='?', type=float, default=18.0,
                        help='The margin for the files. 13 and 18 are quite favorite.')
    parser.add_argument('-fa', '--filename_append', dest='filename_append', nargs='?', type=str, default='_cropped',
                        help='The append to use for the new filenames.')
    parser.add_argument('-r', '--reverse', dest='reverse', nargs='?', type=bool, default=False,
                        help='The pdf origin system is left up instead of left bottom, which is the convention.')
    parser.add_argument('-o', '--order', dest='order', nargs='*', type=int, default=default_order,
                        help='Explicitly set the order of pages on the crop, in case the reverse doesn\'t help.')

    args = parser.parse_args()

    input_files = args.input
    margin = args.margin
    filename_append = args.filename_append
    upside_down = args.reverse
    order = args.order

    width_margin = margin
    height_margin = margin

    for input_file in input_files:
        output_file = '%s%s.pdf' % (input_file[:-4], filename_append)

        input1 = PdfFileReader(open(input_file, 'rb'))
        input2 = PdfFileReader(open(input_file, 'rb'))
        input3 = PdfFileReader(open(input_file, 'rb'))
        input4 = PdfFileReader(open(input_file, 'rb'))

        output = PdfFileWriter()
        output_stream = open(output_file, 'wb')

        pages = input1.getNumPages()

        top_right = (input1.getPage(1).mediaBox.getUpperRight_x() - width_margin,
                     input1.getPage(1).mediaBox.getUpperRight_y() - height_margin)
        top_left = (input1.getPage(1).mediaBox.getUpperLeft_x() + width_margin,
                    input1.getPage(1).mediaBox.getUpperLeft_y() - height_margin)
        bottom_right = (input1.getPage(1).mediaBox.getLowerRight_x() - width_margin,
                        input1.getPage(1).mediaBox.getLowerRight_y() + height_margin)
        bottom_left = (input1.getPage(1).mediaBox.getLowerLeft_x() + width_margin,
                       input1.getPage(1).mediaBox.getLowerLeft_y() + height_margin)

        middle_right = (top_right[0], bottom_right[1] + (top_right[1] - bottom_right[1]) / 2)
        middle_left = (top_left[0], bottom_left[1] + (top_left[1] - bottom_left[1]) / 2)
        top_middle = (top_left[0] + (top_right[0] - top_left[0]) / 2, top_left[1])
        bottom_middle = (bottom_left[0] + (bottom_right[0] - bottom_left[0]) / 2, bottom_left[1])

        middle = (top_middle[0], middle_left[1])

        for i in range(0, pages):
            page1 = input1.getPage(i)
            page1.mediaBox.upperLeft = top_left
            page1.mediaBox.upperRight = top_middle
            page1.mediaBox.lowerLeft = middle_left
            page1.mediaBox.lowerRight = middle

            page2 = input2.getPage(i)
            page2.mediaBox.upperLeft = top_middle
            page2.mediaBox.upperRight = top_right
            page2.mediaBox.lowerLeft = middle
            page2.mediaBox.lowerRight = middle_right

            page3 = input3.getPage(i)
            page3.mediaBox.upperLeft = middle_left
            page3.mediaBox.upperRight = middle
            page3.mediaBox.lowerLeft = bottom_left
            page3.mediaBox.lowerRight = bottom_middle

            page4 = input4.getPage(i)
            page4.mediaBox.upperLeft = middle
            page4.mediaBox.upperRight = middle_right
            page4.mediaBox.lowerLeft = bottom_middle
            page4.mediaBox.lowerRight = bottom_right

            if order is not default_order:
                [output.addPage([page1, page2, page3, page4][i - 1]) for i in order]
            elif upside_down:
                output.addPage(page3)
                output.addPage(page1)
                output.addPage(page4)
                output.addPage(page2)
            else:
                output.addPage(page1)
                output.addPage(page2)
                output.addPage(page3)
                output.addPage(page4)

        output.write(output_stream)
        output_stream.close()
