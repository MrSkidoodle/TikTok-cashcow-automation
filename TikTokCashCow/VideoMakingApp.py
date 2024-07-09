import argparse
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip

file = open("log.txt", 'w')

def main():
    MovieClip = findFileLocation()
    file.write(f"Found File directory: {MovieClip} \n")
    VideoMovieClip = VideoFileClip(MovieClip)
    file.write(f"Created VideoFileClipType \n")
    MovieClip_name = os.path.basename(MovieClip)
    file.write(f"Found File name: {MovieClip_name} \n")
    GamingClip = VideoFileClip(r"C:\Users\Public\script\GamingClip.mp4")
    ConcatenateVideos(VideoMovieClip, GamingClip)
    FinalVideo = VideoFileClip("combined_video.mp4")
    SplitVideo(FinalVideo, MovieClip)


def ConcatenateVideos(VideoMovieClip, GamingClip):
    num_loops = int(VideoMovieClip.duration / GamingClip.duration) + 1
    LoopedGamingClip = concatenate_videoclips([GamingClip] * num_loops, method="compose")
    LoopedGamingClip = LoopedGamingClip.subclip(0, VideoMovieClip.duration)
    half_height = VideoMovieClip.h / 2
    half_width = VideoMovieClip.w / 2.5
    VideoMovieClip = VideoMovieClip.resize((half_width, half_height))
    LoopedGamingClip = LoopedGamingClip.resize((half_width, half_height))
    y_pos_top = 0
    y_pos_bottom = half_height
    final_clip = CompositeVideoClip([
        VideoMovieClip.set_position((0, y_pos_top)),
        LoopedGamingClip.set_position((0, y_pos_bottom))
    ], size=(VideoMovieClip.w, VideoMovieClip.h * 2))
    final_clip.write_videofile("combined_video.mp4", codec="libx264", audio_codec="aac")
    file.write(f"Combined videos \n")
def findFileLocation():
    parser = argparse.ArgumentParser(description="Process video file")
    parser.add_argument("video_file", help="Path to the video file")
    args = parser.parse_args()
    video_path = args.video_file
    return video_path

def SplitVideo(VideoMovieClip, MovieClip):
    MainClipDuration = VideoMovieClip.duration
    file.write(f"Found Main Clip Duration: {MainClipDuration} \n")
    SingleClipDuration = 60
    file.write(f"Single Clip Duration = {SingleClipDuration} \n")
    NumberOfClips = int(MainClipDuration / SingleClipDuration)
    file.write(f"File will be split into {NumberOfClips} files \n")
    for i in range(NumberOfClips):
        start_time = i * SingleClipDuration
        end_time = (i + 1) * SingleClipDuration
        part = VideoMovieClip.subclip(start_time, end_time)
        part_filename = f"{os.path.dirname(MovieClip)}/part_{i + 1}.mp4"
        part.write_videofile(part_filename, codec="libx264", audio_codec="aac")

    last_part = VideoMovieClip.subclip(NumberOfClips * SingleClipDuration, MainClipDuration)
    last_part_filename = f"{os.path.dirname(MovieClip)}/part_{NumberOfClips + 1}.mp4"
    last_part.write_videofile(last_part_filename, codec="libx264", audio_codec="aac")

main()

