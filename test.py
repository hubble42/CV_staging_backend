from moviepy.editor import *
# Load the input video file
input_file = VideoFileClip("C:\\Users\\DELL\\object-detection\\backend\\runs\\detect\\predict109\\pexels-free-videos-853889-1920x1080-25fps.mp4")
# Set the output video format and codec
output_format = "mp4"
codec = "libx264"
# Convert the input video to the output format with the specified codec
output_file = input_file.write_videofile("output.mp4", codec=codec, audio_codec="aac",
                                         threads=4, fps=input_file.fps,
                                         preset="medium", ffmpeg_params=["-crf", "23"])
# Close the input and output files
input_file.close()
output_file.close()