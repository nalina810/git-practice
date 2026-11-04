import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw, ImageFont
import math
import os

# Dark to bright characters
ASCII_CHARS = " .,:;irsXA253hMHGS#9B&@"

# Image settings
IMAGE_WIDTH = 200
FONT_SIZE = 4

ascii_pixels = []
animation_running = False
animation_frame = 0


def convert_image(image_path):
    """Convert photograph into detailed grayscale pixel data."""

    image = Image.open(image_path).convert("RGB")

    # Grayscale conversion
    image = ImageOps.grayscale(image)

    # Improve image contrast and details
    image = ImageOps.autocontrast(image, cutoff=2)
    image = ImageEnhance.Contrast(image).enhance(1.8)
    image = ImageEnhance.Brightness(image).enhance(1.1)
    image = ImageEnhance.Sharpness(image).enhance(2.5)

    # Slight noise reduction
    image = image.filter(ImageFilter.MedianFilter(size=3))

    # Resize image
    old_width, old_height = image.size

    new_height = max(
        1,
        int(old_height / old_width * IMAGE_WIDTH * 0.48)
    )

    image = image.resize(
        (IMAGE_WIDTH, new_height),
        Image.Resampling.LANCZOS
    )

    # Extract pixels
    pixels = list(image.get_flattened_data())

    rows = []

    for y in range(new_height):
        start = y * IMAGE_WIDTH
        end = start + IMAGE_WIDTH
        rows.append(pixels[start:end])

    return rows


def generate_ascii(animated=False):
    """Generate ASCII artwork."""

    global animation_frame

    if not ascii_pixels:
        return

    lines = []

    for y, row in enumerate(ascii_pixels):

        line = ""

        for x, original_pixel in enumerate(row):

            pixel = original_pixel

            # Moving light wave
            if animated:
                wave = 15 * math.sin(
                    x * 0.045 + animation_frame * 0.18
                )

                pixel = int(
                    max(0, min(255, pixel + wave))
                )

            # Character mapping
            index = (
                pixel * (len(ASCII_CHARS) - 1) // 255
            )

            line += ASCII_CHARS[index]

        lines.append(line)

    output.config(state="normal")
    output.delete("1.0", tk.END)

    output.insert(
        "1.0",
        "\n".join(lines),
        "center"
    )

    output.config(state="disabled")


def choose_image():
    """Choose an image."""

    global ascii_pixels

    stop_animation()

    image_path = filedialog.askopenfilename(
        title="Choose Your Photograph",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.bmp")
        ]
    )

    if not image_path:
        return

    try:
        ascii_pixels = convert_image(image_path)

        generate_ascii()

        status_label.config(
            text="Image loaded successfully!",
            fg="white"
        )

    except Exception as error:
        messagebox.showerror(
            "Image Error",
            str(error)
        )


def show_static():
    """Show static portrait."""

    stop_animation()

    if not ascii_pixels:
        messagebox.showinfo(
            "Notice",
            "Please choose an image first."
        )
        return

    generate_ascii(animated=False)

    status_label.config(
        text="Static portrait displayed",
        fg="white"
    )


def animation_step():
    """Update animation."""

    global animation_frame

    if not animation_running:
        return

    generate_ascii(animated=True)

    animation_frame += 1

    root.after(120, animation_step)


def start_animation():
    """Start animated portrait."""

    global animation_running, animation_frame

    if not ascii_pixels:
        messagebox.showinfo(
            "Notice",
            "Please choose an image first."
        )
        return

    if animation_running:
        return

    animation_running = True
    animation_frame = 0

    status_label.config(
        text="Animation running...",
        fg="white"
    )

    animation_step()


def stop_animation():
    """Stop animation."""

    global animation_running

    animation_running = False

    if ascii_pixels:
        generate_ascii(animated=False)

        status_label.config(
            text="Animation stopped",
            fg="white"
        )


def save_artwork():
    """Save ASCII artwork as TXT or PNG."""

    if not ascii_pixels:
        messagebox.showinfo(
            "Notice",
            "Please choose an image first."
        )
        return

    file_path = filedialog.asksaveasfilename(
        title="Save ASCII Artwork",
        defaultextension=".png",
        filetypes=[
            ("PNG Image", "*.png"),
            ("Text File", "*.txt")
        ]
    )

    if not file_path:
        return

    try:
        artwork = output.get(
            "1.0",
            tk.END
        ).rstrip("\n")

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".txt":

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:
                file.write(artwork)

            messagebox.showinfo(
                "Success",
                "ASCII artwork saved as TXT!"
            )

        elif extension == ".png":

            # Load monospace font
            try:
                font = ImageFont.truetype(
                    "C:/Windows/Fonts/consola.ttf",
                    12
                )
            except OSError:
                font = ImageFont.load_default()

            # Calculate image dimensions
            temporary_image = Image.new(
                "RGB",
                (1, 1),
                "black"
            )

            draw = ImageDraw.Draw(temporary_image)

            bbox = draw.multiline_textbbox(
                (0, 0),
                artwork,
                font=font,
                spacing=0
            )

            width = bbox[2] - bbox[0] + 40
            height = bbox[3] - bbox[1] + 40

            # Create black background
            image = Image.new(
                "RGB",
                (width, height),
                "black"
            )

            draw = ImageDraw.Draw(image)

            # Draw white ASCII characters
            draw.multiline_text(
                (20 - bbox[0], 20 - bbox[1]),
                artwork,
                font=font,
                fill="white",
                spacing=0
            )

            image.save(file_path)

            messagebox.showinfo(
                "Success",
                "ASCII portrait saved as PNG!"
            )

        else:
            messagebox.showerror(
                "Error",
                "Please save using PNG or TXT format."
            )

    except Exception as error:
        messagebox.showerror(
            "Save Error",
            str(error)
        )


# ---------------- MAIN APPLICATION ----------------

root = tk.Tk()

root.title("ASCII Portrait Generator - Version 5.1")
root.geometry("1200x850")
root.configure(bg="#080808")


# Heading
heading = tk.Label(
    root,
    text="ASCII PORTRAIT GENERATOR",
    font=("Arial", 25, "bold"),
    fg="white",
    bg="#080808"
)

heading.pack(pady=(15, 5))


subtitle = tk.Label(
    root,
    text="Transform photographs into detailed ASCII portraits",
    font=("Arial", 11),
    fg="#cccccc",
    bg="#080808"
)

subtitle.pack(pady=5)


# Buttons
button_frame = tk.Frame(
    root,
    bg="#080808"
)

button_frame.pack(pady=15)


def make_button(text, command):
    return tk.Button(
        button_frame,
        text=text,
        command=command,
        font=("Arial", 10, "bold"),
        bg="#252525",
        fg="white",
        activebackground="#444444",
        activeforeground="white",
        padx=12,
        pady=9,
        relief="flat",
        cursor="hand2"
    )


make_button(
    "Choose Image",
    choose_image
).grid(row=0, column=0, padx=5)

make_button(
    "Static Portrait",
    show_static
).grid(row=0, column=1, padx=5)

make_button(
    "Start Animation",
    start_animation
).grid(row=0, column=2, padx=5)

make_button(
    "Stop Animation",
    stop_animation
).grid(row=0, column=3, padx=5)

make_button(
    "Save Artwork",
    save_artwork
).grid(row=0, column=4, padx=5)


# Display area
display_frame = tk.Frame(
    root,
    bg="#080808"
)

display_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)


# Scrollbars
vertical_scroll = tk.Scrollbar(display_frame)

vertical_scroll.pack(
    side="right",
    fill="y"
)

horizontal_scroll = tk.Scrollbar(
    display_frame,
    orient="horizontal"
)

horizontal_scroll.pack(
    side="bottom",
    fill="x"
)


# ASCII output
output = tk.Text(
    display_frame,
    bg="black",
    fg="white",
    insertbackground="white",
    font=("Consolas", FONT_SIZE),
    wrap="none",
    padx=10,
    pady=10,
    spacing1=0,
    spacing2=0,
    spacing3=0,
    yscrollcommand=vertical_scroll.set,
    xscrollcommand=horizontal_scroll.set,
    state="disabled"
)

output.pack(
    side="left",
    fill="both",
    expand=True
)


# Centre-align ASCII portrait
output.tag_configure(
    "center",
    justify="center"
)


vertical_scroll.config(
    command=output.yview
)

horizontal_scroll.config(
    command=output.xview
)


# Status label
status_label = tk.Label(
    root,
    text="Choose an image to get started",
    font=("Arial", 10),
    fg="white",
    bg="#080808"
)

status_label.pack(pady=10)


# Start application
root.mainloop()