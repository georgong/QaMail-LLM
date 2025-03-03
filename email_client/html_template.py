email_template = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{subject}</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 20px;
                        background-color: #f4f4f4 !important;
                    }}
                    .email-container {{
                        background-color: #fff !important;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }}
                    .email-subject {{
                        font-size: 24px;
                        color: #333;
                        margin-bottom: 10px;
                    }}
                    .email-content {{
                        font-size: 16px;
                        color: #555;
                        line-height: 1.6;
                    }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="email-subject">{subject}</div>
                    <div class="email-content">{text_content}</div>
                </div>
            </body>
            </html>
            """