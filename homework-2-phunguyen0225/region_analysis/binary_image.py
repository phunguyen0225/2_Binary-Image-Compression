class BinaryImage:
    def __init__(self):
        pass

    def compute_histogram(self, image):
        """Computes the histogram of the input image
        takes as input:
        image: a grey scale image
        returns a histogram as a list"""
        (row, col) = image.shape
        hist = [0]*256

        for i in range(row):
            for j in range(col):
                hist[image[i, j]] += 1
        return hist

    def find_otsu_threshold(self, hist):
        """analyses a histogram to find the otsu's threshold assuming that the input histogram is bimodal.
        takes as input
        hist: a histogram
        returns: an optimal threshold value (otsu's threshold)"""
        threshold = 0
        total_pixel = 0
        for i in hist:
            total_pixel += i
        probabilities = {}
        for i in range(0,255):
            probabilities[i] = hist[i]/total_pixel

        threshold_dict = {}
        for num in range(0, 255):
            #weight
            q1 = 0 
            q2 = 0

            #means
            u1_total = 0
            u1_vals = 0
            u2_total = 0
            u2_vals = 0

            #variance
            o1 = 0
            o2 = 0
            for t in range(0, num):
                #calculating q1 
                q1 += probabilities[t]
                u1_vals += hist[t] * t
                u1_total += hist[t]

            q1 /= total_pixel

            if u1_total > 0:
                mean1 = u1_vals / u1_total
                for i in range(0, num):
                    o1 += ((i - mean1) ** 2) * hist[i]

            if u1_total > 0:
                o1 /= u1_total

            for t in range(num+1, 255):
                q2 += probabilities[t]
                u2_vals += hist[t] * t
                u2_total += hist[t]

            q2 /= total_pixel
            if u2_total > 0:
                mean2 = u2_vals / u2_total
                for i in range(num + 1, 255):
                    o2 += ((i - mean2) ** 2) * hist[i]

            if u2_total > 0 :
                o2 /= u2_total
                class_variance = q1 * o1 + q2 * o2
                threshold_dict[num] = class_variance
        threshold = min(threshold_dict.keys(), key=(lambda k: threshold_dict[k]))
        return threshold
        

    def binarize(self, image):
        """Comptues the binary image of the the input image based on histogram analysis and thresholding
        Make calls to the compute_histogram and find_otsu_threshold methods as needed.
        takes as input
        image: an grey scale image
        returns: a binary image"""

        bin_img = image.copy()
        hist = self.compute_histogram(image)
        threshold = self.find_otsu_threshold(hist)

        for i in range(bin_img.shape[0]):
            for j in range(bin_img.shape[1]):
                if (bin_img[i, j] > threshold): # '1' black , 0 - black
                    bin_img[i, j] = 0 
                elif (bin_img[i, j] <= threshold): # '0' - white,  255- white
                    bin_img[i, j] = 255
        return bin_img
