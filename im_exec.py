import os
import subprocess
import tkinter

# os.environ["MAGICK_HOME "] = os.getcwd() + R"\imageMagick"


def compress_dir_jpg(
    source_dir: str,
    output_dir: str,
    label_var: tkinter.StringVar,
    label_current_no: tkinter.StringVar,
    progress_bar_fn,
    compress_btn_handle: tkinter.Button,
    error_var: tkinter.StringVar,
    extension: str = ".jpg",
):  
    try:
        source_dir = source_dir.rstrip("\\")
        total_count = calculate_images(source_dir, extension)
        cmd = (
            os.getcwd()
            + "\\imageMagick\\magick mogrify -path "
            + '"'
            + output_dir
            + '"'
            + " -resize 3840x2160^ -filter Triangle -define filter:support=2 -unsharp 0.25x0.08+8.3+0.045 -dither None -quality 82 -define jpeg:fancy-upsampling=off -define png:compression-filter=5 -define png:compression-level=9 -define png:compression-strategy=1 -interlace none -colorspace sRGB -clamp -verbose "
            + '"'
            + source_dir
            + "\\*"
            + extension
            + '"'
        )
        print(cmd)
        # execute_fn()
        prev_filename = ""
        image_counter = 0
        label_var.set("ROZPOCZĘTO")
        label_current_no.set("0/" + str(total_count))
        for line in execute(cmd):
            if line == 1:
                error_var.set("Coś poszło nie tak")
                break
            filename = extract_filename(line, extension)
            if filename != extension:
                label_var.set(filename + extension)
                if filename != prev_filename:
                    prev_filename = filename
                    image_counter += 1
                    label_current_no.set(str(image_counter) + "/" + str(total_count))
                    progress_bar_fn(float(image_counter / total_count))
    except Exception as e:
        error_var.set("Coś poszło nie tak")

    label_var.set("ZAKOŃCZONO")
    label_current_no.set("")
    compress_btn_handle.configure(state=tkinter.NORMAL)


def calculate_images(source_dir, extension):
    extension = extension.lower()

    onlyfiles_with_ext = [
        f
        for f in os.listdir(source_dir)
        if os.path.isfile(os.path.join(source_dir, f)) and extension in f.lower()
    ]

    return len(onlyfiles_with_ext)


def extract_filename(line, extension):
    line_lower = line.lower()
    filename = line[line_lower.rindex("\\") + 1 : line_lower.rindex(extension)]
    return filename


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        yield return_code
        raise subprocess.CalledProcessError(return_code, cmd)


if __name__ == "__main__":
    source_dir = (
        "D:\OneDrive - Politechnika Wroclawska\projectsPython\imageCompressor\images_in"
    )
    output_dir = "D:\OneDrive - Politechnika Wroclawska\projectsPython\imageCompressor\images_out"
    # extract_filename(
    #     R"D:\OneDrive - Politechnika Wroclawska\projectsPython\imageCompressor\images_in\P5130202.JPG JPEG 4608x3456 4608x3456+0+0 8-bit sRGB 6.83107MiB 0.172u 0:00.170>3840x2880 3840x2880+0+0 8-bit sRGB 860718B 1.313u 0:01.319",
    #     ".jpg",
    # )
    print(calculate_images(source_dir, ".jpg"))
    # compress_dir_jpg(
    #     source_dir=source_dir,
    #     output_dir=output_dir,
    #     progress_bar_fn=None,
    #     compress_btn_handle=None,
    #     label_var=None,
    # )
