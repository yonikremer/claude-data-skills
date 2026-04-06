import extract_msg
import os

def extract_msg_content(msg_path, output_dir):
    """
    Extracts body and attachments from an MSG file.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    msg = extract_msg.Message(msg_path)
    
    # Save text content
    with open(os.path.join(output_dir, "body.txt"), "w", encoding="utf-8") as f:
        f.write(msg.body)
    
    # Save attachments
    for attachment in msg.attachments:
        attachment_path = os.path.join(output_dir, attachment.getFilename())
        attachment.save(customPath=attachment_path)
        print(f"Extracted attachment: {attachment.getFilename()}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python extract_emails.py <path_to_msg> <output_dir>")
        sys.exit(1)
    
    extract_msg_content(sys.argv[1], sys.argv[2])
