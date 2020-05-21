import cv2
import os
import time

import argparse

class CameraDataCreator:

    def __init__(self , dst , total_save ,time_diff = 0.5):

        if os.path.isdir(dst) == False:
            os.makedirs(dst)

        self.last_recoded_time = None
        self.dst = dst
        self.time_diff = time_diff
        self.total_save = total_save

    def run(self , video_src ,  size):

        frame_delay = 1
        self.is_video_file = False

        try:
            video_src = int(video_src)
        except ValueError:
            frame_delay = 45
            self.is_video_file = True



        cap = cv2.VideoCapture(video_src)
        video_running = True

        index = 0

        while video_running:

            ret , current_frame = cap.read()

            if ret == False:
                print("Video stoped")
                video_running = False
                continue

            current_frame = cv2.resize(current_frame , size)

            if self._should_save():
                self._save(index , current_frame)
                index += 1
                print("{} data saved".format(index))

                if self._is_finished(index):
                    print("Total {} image saved.".format(self.total_save))
                    video_running = False

            cv2.imshow("Image" , current_frame)


            if cv2.waitKey(frame_delay) & 0xFF == ord("q"):
                video_running = False


        self._close(cap)

    def _close(self , cap):
        cap.release()
        cv2.destroyAllWindows()

    def _is_finished(self , frame_index):

        '''
        If its a video file, we want to finish the whole video
        '''

        if self.is_video_file:
            return False


        return frame_index == self.total_save


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

    parser = argparse.ArgumentParser()
    parser.add_argument("-v" , "--video" , default = "1", help = "Video Src")
    parser.add_argument("-d" , "--dst" , default = "Test", help = "Dst for image to save")
    parser.add_argument("-ts" , "--total_save" , type = int , default = 50 , help = "number of image to save")
    parser.add_argument("-s" , "--size" , type = int , default = 224 , help = "Image save size")
    parser.add_argument("-td" , "--time_diff" , type = float , default = 1, help = "Frame diff between save")
    args = parser.parse_args()

    camera = CameraDataCreator(args.dst  , total_save = args.total_save)
    camera.run(video_src = args.video , size = (args.size , args.size))


if __name__ == "__main__":
    main()





