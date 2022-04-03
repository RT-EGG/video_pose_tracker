import os
from abc import abstractmethod

import sys
import cv2
import mediapipe
import moviepy.editor as movie_editor
import numpy as np
import tqdm


class VideoConverter:
    def __init__(self, in_input_filepath):
        self.input_filepath = in_input_filepath
        self.video = cv2.VideoCapture(self.input_filepath)
        self.format = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        self.save_audio = True
        
        self.mp_drawing = mediapipe.solutions.drawing_utils
        self.mp_drawing_styles = mediapipe.solutions.drawing_styles
        self.mp_pose = mediapipe.solutions.pose

        print('initialize model instance.')
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=2,
            enable_segmentation=self._do_enable_segmentation(),
            min_detection_confidence=0.5
        )

    def execute(self, in_output_filepath):
        frame_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        new_frames = []

        empty = np.zeros((300, 300, 3), dtype=np.uint8)
        empty[:] = (0, 0, 0)
        self.pose.process(empty)

        print('convert frames.')
        for i in tqdm.tqdm(range(frame_count)):
            _, frame = self.video.read()            

            tracked_pose = self.pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if self._do_enable_segmentation():
                new_frame = self._convert_image(frame, tracked_pose.segmentation_mask)
            else:
                new_frame = self._convert_image(frame, tracked_pose.pose_landmarks)

            new_frames.append(new_frame)

        writer = cv2.VideoWriter(
            in_output_filepath, 
            self.format, 
            int(self.video.get(cv2.CAP_PROP_FPS)),
            (
                int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            )
        )

        print('write file.')
        for i in tqdm.tqdm(range(frame_count)):
            writer.write(new_frames[i])
        writer.release()

        if self.save_audio:
            print('write audio.')
            audio_filepath = os.path.splitext(in_output_filepath)[0]
            audio_filepath = f"{audio_filepath}_audio.mp3"
            renamed_movie_filepath = os.path.splitext(in_output_filepath)[0]
            renamed_movie_filepath = f"{renamed_movie_filepath}_tmp.mp4"

            if os.path.isfile(audio_filepath):
                os.remove(audio_filepath)
            if os.path.isfile(renamed_movie_filepath):
                os.remove(renamed_movie_filepath)

            os.rename(in_output_filepath, renamed_movie_filepath)

            input_clip = movie_editor.VideoFileClip(self.input_filepath)
            input_clip.audio.write_audiofile(audio_filepath)

            output_clip = movie_editor.VideoFileClip(renamed_movie_filepath).subclip()
            output_clip.write_videofile(in_output_filepath, audio=audio_filepath)

            os.remove(renamed_movie_filepath)
            os.remove(audio_filepath)

    @abstractmethod
    def _convert_image(self, in_image, in_landmarks):
        return in_image.copy()

    @abstractmethod
    def _do_enable_segmentation(self):
        return False
    
class VideoPoseConverter(VideoConverter):
    def __init__(self, in_video):
        super().__init__(in_video)

    def _convert_image(self, in_image, in_landmarks):
        tracked = np.zeros(in_image.shape, dtype=np.uint8)
        tracked[:] = (0, 0, 0)
        if in_landmarks:
            self.mp_drawing.draw_landmarks(
                tracked,
                in_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec = self.mp_drawing_styles.get_default_pose_landmarks_style()
            )

        return tracked

    def _do_enable_segmentation(self):
        return super()._do_enable_segmentation()

class VideoOverlayConverter(VideoConverter):
    def __init__(self, in_video):
        super().__init__(in_video)

    def _convert_image(self, in_image, in_landmarks):
        image = in_image.copy()
        
        if in_landmarks:
            self.mp_drawing.draw_landmarks(
                image,
                in_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec = self.mp_drawing_styles.get_default_pose_landmarks_style()
            )

        return image

    def _do_enable_segmentation(self):
        return super()._do_enable_segmentation()

class VideoSegmentationConverter(VideoConverter):
    def __init__(self, in_input_filepath, in_background_image):
        super().__init__(in_input_filepath)

        self.background_image = in_background_image

    def _convert_image(self, in_image, in_segmentation_mask):
        if in_segmentation_mask is not None:
            if not np.all(in_image.shape == self.background_image.shape):
                raise RuntimeError('Dimensions of images between video and background must be same.')

            condition = np.stack((in_segmentation_mask,) * 3, axis=-1) < 0.1
            return np.where(condition, in_image, self.background_image)
        return in_image.copy()

    def _do_enable_segmentation(self):
        return True
