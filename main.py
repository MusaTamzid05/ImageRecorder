import cv2
import os
import time

class CameraDataCreator:

    def __init__(self , dst , time_diff = 0.5):

        if os.path.isdir(dst) == False:
            os.makedirs(dst)

        self.last_recoded_time = None
        self.dst = dst
        self.time_diff = time_diff

    def run(self , size):

        cap = cv2.VideoCapture(0)
        video_running = True

        index = 0

        while video_running:

            ret , current_frame = cap.read()

            if ret == False:
                video_running = False
                continue

            current_frame = cv2.resize(current_frame , size)

            if self._should_save():
                self._save(index , current_frame)
                print("Data saved")
                index += 1

            cv2.imshow("Image" , current_frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cap.release()
                cv2.destroyAllWindows()
                video_running = False

    def _save(self , frame_index ,  image):

        path_data  = self.dst.split("/")
        label = path_data[len(path_data) - 1]
        dst_filepath = os.path.join(self.dst , label + "_" + str(frame_index)+ ".jpg")

        cv2.imwrite(dst_filepath, image)

    def _should_save(self):

        current_time = time.time()

        if self.last_recoded_time is None:
            self.last_recoded_time = current_time
            return True

        current_time_diff = current_time - self.last_recoded_time

        if  current_time_diff > self.time_diff:
            self.last_recoded_time = current_time
            return True

        return False






def main():

    camera = CameraDataCreator("./test")
    camera.run(size = (224 , 224))


if __name__ == "__main__":
    main()





