#!/usr/bin/env python

from PyPDF2 import PdfFileWriter, PdfFileReader
import argparse

__author__ = 'Gyfis'


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Easily crop slides from your favorite teacher - BartaK!")
    parser.add_argument('input', nargs='*', help='The files you want to convert.')
    parser.add_argument('-m', '--margin', type=float, default=18.0,
                        help='The margin for the files. 13 and 18 are quite favorite.')
    parser.add_argument('-fa', '--filename-append', default='_cropped',
                        help='The append to use for the new filenames.')
    parser.add_argument('-r', '--reverse', action='store_true',
                        help='The pdf origin system is left up instead of left bottom, which is the convention.')
    parser.add_argument('-o', '--order', nargs=4, type=int, default=[1, 2, 3, 4],
                        help='Explicitly set the order of pages on the crop, in case the reverse doesn\'t help.')

    args = parser.parse_args()

    input_files = args.input
    margin = args.margin
    filename_append = args.filename_append
    order = args.order

    if args.reverse:
        order = [order[i-1] for i in [3, 1, 4, 2]]

    width_margin = margin
    height_margin = margin

    for input_file in input_files:
        output_file = '%s%s.pdf' % (input_file[:-4], filename_append)

        input1 = PdfFileReader(open(input_file, 'rb'))
        input2 = PdfFileReader(open(input_file, 'rb'))
        input3 = PdfFileReader(open(input_file, 'rb'))
        input4 = PdfFileReader(open(input_file, 'rb'))

        output = PdfFileWriter()
        with open(output_file, 'wb') as output_stream:

            top_right = (float(input1.getPage(1).mediaBox.getUpperRight_x()) - width_margin,
                         float(input1.getPage(1).mediaBox.getUpperRight_y()) - height_margin)
            top_left = (float(input1.getPage(1).mediaBox.getUpperLeft_x()) + width_margin,
                        float(input1.getPage(1).mediaBox.getUpperLeft_y()) - height_margin)
            bottom_right = (float(input1.getPage(1).mediaBox.getLowerRight_x()) - width_margin,
                            float(input1.getPage(1).mediaBox.getLowerRight_y()) + height_margin)
            bottom_left = (float(input1.getPage(1).mediaBox.getLowerLeft_x()) + width_margin,
                           float(input1.getPage(1).mediaBox.getLowerLeft_y()) + height_margin)

            middle_right = (top_right[0], bottom_right[1] + (top_right[1] - bottom_right[1]) / 2)
            middle_left = (top_left[0], bottom_left[1] + (top_left[1] - bottom_left[1]) / 2)
            top_middle = (top_left[0] + (top_right[0] - top_left[0]) / 2, top_left[1])
            bottom_middle = (bottom_left[0] + (bottom_right[0] - bottom_left[0]) / 2, bottom_left[1])

            middle = (top_middle[0], middle_left[1])

            for i in range(input1.getNumPages()):
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

                pages = [page1, page2, page3, page4]

                for i in order:
                    output.addPage(pages[i-1])

            output.write(output_stream)
