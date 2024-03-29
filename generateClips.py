import os
from moviepy.editor import VideoFileClip, ImageClip, TextClip, CompositeVideoClip

def createTitleClip(wrappedText, start, duration):
    width_x = 1080
    height_y = 1920
    textbox_size_x = 900
    textbox_size_y = 600
    center_x = width_x / 2 - textbox_size_x / 2
    center_y = height_y / 2 - textbox_size_y / 2
    font = "ARLRDBD.TTF"
    new_textclip = TextClip(
        wrappedText, 
        fontsize=50, 
        color='black', 
        bg_color='transparent',
        method='caption',
        font=f"static/fonts/{font}",
        size=(820, None),
        align='West',
    ).set_start(start).set_duration(duration).resize(width=820).set_position(('center', 'center'))

    text_width, text_height = new_textclip.size

    background_clip = TextClip(
        "", 
        fontsize=50, 
        color='white', 
        bg_color='white',
        method='caption',
        font=f"static/fonts/{font}",
        size=(900, text_height + 20),
        align='West',
    ).set_start(start).set_duration(duration).set_position(('center', 'center'))

    banner_path = 'static/images/medalled_banner_resized.png'
    banner_clip = ImageClip(banner_path, duration=duration).resize(width=900)
    banner_clip = banner_clip.set_pos((center_x, height_y / 2 - (text_height / 2) - banner_clip.size[1] - 10))

    comment_path = 'static/images/comments.png'
    comment_clip = ImageClip(comment_path, duration=duration).resize(width=900)
    comment_clip = comment_clip.set_pos((center_x, height_y / 2 + (text_height / 2) + 10))

    return background_clip, new_textclip, banner_clip, comment_clip

def createTextClip(wrappedText, start, duration, color='white'):
    width_x = 1080
    height_y = 1920
    textbox_size_x = 900
    textbox_size_y = 600
    center_x = width_x / 2 - textbox_size_x / 2
    center_y = height_y / 2 - textbox_size_y / 2

    font = 'GILBI___.TTF'
    new_textclip = TextClip(
        wrappedText, 
        fontsize=105, 
        color=color, 
        bg_color='transparent',
        method='caption',
        # method='label',
        font=f'static/fonts/{font}',
        size=(textbox_size_x, None)#, textbox_size_y)
    ).set_start(start).set_duration(duration).resize(lambda t : min(1, 0.8  + 15 * t)).set_position(('center', 'center'))
    
    shadow_textclip = TextClip(
        wrappedText, 
        fontsize=105, 
        color='black', 
        bg_color='transparent', 
        stroke_width=20,
        stroke_color="black",
        method='caption',
        # method='label',
        font=f'static/fonts/{font}',
        size=(textbox_size_x + 20, None)#, textbox_size_y)
    ).set_start(start).set_duration(duration).resize(lambda t : min(1, 0.6  + 20 * t)).set_position(('center', 'center'))

    return new_textclip, shadow_textclip

if __name__ == "__main__":
    # title page test
    # background_clip, new_textclip, banner_clip, comment_clip = createTitleClip("UPDATE: How can I (M40) explain to my kids (F12/15/17) that my infidelity is the cause of our divorce?\n(part 1)", 0, 5)
    # background_clip, new_textclip, banner_clip, comment_clip = createTitleClip("UPDATE: How can I (M40) explain to my kids that my infedelitys (p1)", 0, 5)
    # input_video_path = 'AITAH1.mp4'
    # video_clip = VideoFileClip(input_video_path)
    # segment_clip = video_clip.subclip(0, 5)
    # video_with_text = CompositeVideoClip([segment_clip] + [background_clip, new_textclip, banner_clip, comment_clip])
    # video_with_text.write_videofile("test.mp4", codec="libx264", threads=8, preset='ultrafast', logger = None)

    # text scale test
    new_textclip, shadow_textclip = createTextClip("How can I (M40) explain to my kids", 0, 5)
    input_video_path = 'AITAH1.mp4'
    video_clip = VideoFileClip(input_video_path)
    segment_clip = video_clip.subclip(0, 5)
    video_with_text = CompositeVideoClip([segment_clip] + [shadow_textclip, new_textclip])
    video_with_text.write_videofile("test.mp4", codec="libx264", threads=8, preset='ultrafast', logger = None)