import cv2
class CellCounting:
    def __init__(self):
        pass

    def blob_coloring(self, image):
        """Uses the blob coloring algorithm based on 5 pixel cross window and assigns region names
        takes a input:
        image: binary image
        return: a list/dict of regions"""
        
        temp = [ [0] * len(image[0]) for _ in range(len(image))]
        counter = 1
        region = dict()
        for row in range(0, len(image)):
            for col in range(0, len(image[0])):
                if row == 0 and col == 0:
                    if image[row][col] == 0:
                        temp[row][col] = counter
                        counter += 1
                elif row == 0:
                    if image[row][col] == 0 and image[row][col - 1] == 0:
                        temp[row][col] = temp[row][col - 1]
                elif col == 0:
                    if image[row][col] == 0 and image[row - 1][col] == 0:
                        temp[row][col] = temp[row - 1][col]
                else:
                    if image[row][col] == 0 and image[row][col - 1] == 255 and image[row - 1][col] == 255:
                        temp[row][col] = counter
                        counter += 1
                    if image[row][col] == 0 and image[row][col - 1] == 255 and image[row - 1][col] == 0:
                        temp[row][col] = temp[row - 1][col]
                    if image[row][col] == 0 and image[row][col - 1] == 0 and image[row - 1][col] == 255:
                        temp[row][col] = temp[row][col - 1]
                    if image[row][col] == 0 and image[row][col - 1] == 0 and image[row - 1][col] == 0:
                        temp[row][col] = temp[row - 1][col]
                        if temp[row][col - 1] != temp[row - 1][col]:
                            for x in range(0, row):
                                for y in range(0, col):
                                    if temp[x][y] == temp[row][col - 1]:
                                        temp[x][y] = temp[row - 1][col]

        for row in range(0,len(temp)):
            for col in range(0,len(temp[0])):
                if temp[row][col] in region.keys() and temp[row][col] != 0:
                    region.setdefault(temp[row][col], []).append([row, col])
                elif temp[row][col] != 0:
                    region[temp[row][col]] = [[row, col]]

        return region
    

    def compute_statistics(self, region):
        """Computes cell statistics area and location
        takes as input
        region: list regions and corresponding pixels
        returns: stats"""
        
        count = 0
        stats = []

        for key in region.keys():
            if len(region[key]) > 15:
                area = len(region[key])
                pixels = region[key]
                x = 0
                y = 0
                count += 1
                for points in pixels:
                    x += points[0]
                    y += points[1]
                x /= len(region[key])
                y /= len(region[key])
                center =(int(x),int(y))
                stats.append([count,area,center])
                print("Region: ", count, "Area: ", area, "Center", center)
    

        return stats
        
    def mark_image_regions(self, image, stats):
        """Creates a new image with computed stats
        Make a copy of the image on which you can write text. 
        takes as input
        image: Input binary image
        stats: stats regarding location and area
        returns: image marked with center and area"""
        
        for line in stats:
            area = str(line[1])
            centroid = line[2]
            font = cv2.FONT_HERSHEY_SIMPLEX
            color = (255, 0,0)
            image = cv2.putText(image,"*", (centroid[0],centroid[1]),font,0.25,color,2)
            image = cv2.putText(image,area, (centroid[0]+2,centroid[1]+2),font,0.5,color,2)


        return image
        
