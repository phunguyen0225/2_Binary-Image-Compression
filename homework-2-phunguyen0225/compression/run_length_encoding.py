import numpy as np

class Rle:
    def __init__(self):
        pass

    def encode_image(self,binary_image):
        """
        For efficiency, flatten the image by concatinating rows to create one long array, and
        compute run length encoding.
        Compress the image
        takes as input:
        image: binary_image
        returns run length code
        """
        #store the encoding list
        encoding_list = []
        #counter
        count = 1
    
        for row in range(binary_image.shape[0]):
            #gets the first pixel value of every row
            first = binary_image[row, 0]

            #encodes 1 if black, 0 if white
            if first == 0:
                encoding_list.append(1)
            else:
                encoding_list.append(0)
            for col in range(binary_image.shape[1]-1):
                #for the right border
                if binary_image[row, col+1] == binary_image[row, col]:
                    #keeps incrementing until it finds a different value
                    count += 1
                    #appends final blob at the end of the column if necessary
                    if ((col+1) == binary_image.shape[1]-1) and (binary_image[row, col+1] == binary_image[row, col]):
                        encoding_list.append(count)
                        #resets counter and updates previous element position
                        count = 1
                else:
                    encoding_list.append(count)
                    #resets counter and updates previous element position
                    count = 1
                    #if blob does not touch rightmost pixel in image border in row
                    if ((col+1) == binary_image.shape[1]-1) and (binary_image[row, col+1] != binary_image[row, col]):
                        count = 1
                        encoding_list.append(count)
                        #resets counter and updates previous element position
                        count = 1
    
        return encoding_list

    def decode_image(self, rle_code, height , width):
        """
        Since the image was flattened during the encoding, use the hight and width to reconstruct the image
        Reconstructs original image from the rle_code
        takes as input:
        rle_code: the run length code to be decoded
        Height, width: height and width of the original image
        returns decoded binary image
        """

        #creates base image
        image = np.zeros((height,width), np.uint8)
        
        #moves through rle code
        i = 0
        
        for row in range(height):
            #resets column counter
            col = 0
            #gets first pixel value
            pixelValue = rle_code[i]
            if pixelValue == 0:
                value = 255
            else:
                value = 0
            #used while loop here to change the col integer in loop
            while col < width:
                i += 1
                num = 0
                #gets number of occurrences of value
                num = rle_code[i]
                #only changes pixels that are white
                for j in range(num):
                    image[row, col] = value
                    col += 1
                    #error checking for bound
                    if col == width:
                        break
                    
                #swaps color for next write
                if value == 0:
                    value = 255
                else:
                    value = 0
            
            #gets next pixel value
            i += 1
                
        return image