import cv2
import os
import time

class CameraDataCreator:

    def __init__(self , dst):

        if os.path.isdir(dst) == False:
            os.makedirs(dst)

        self.dst = dst

    def run(self , size ,  time_diff = 0.5):

        cap = cv2.VideoCapture(0)
        video_running = True

        index = 0

        while video_running:

            ret , current_frame = cap.read()

            if ret == False:
                video_running = False
                continue

            current_frame = cv2.resize(current_frame , size)

            cv2.imshow("Image" , current_frame )
            path_data  = self.dst.split("/")
            label = path_data[len(path_data) - 1]
            dst_filepath = os.path.join(self.dst , label + "_" + str(index)+ ".jpg")

            cv2.imwrite(dst_filepath, current_frame)
            index += 1

            if cv2.waitKey(1) & 0xFF == ord("q"):
                cap.release()
                cv2.destroyAllWindows()
                video_running = False



def main():

    camera = CameraDataCreator("./test")
    camera.run(size = (224 , 224))


if __name__ == "__main__":
    main()





