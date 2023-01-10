import sys

from google_reviews.models.reviews import Review


def process_data(text: str) -> list:
    """

    :param text:
    :return:
    """
    data = text.split(',[[[')
    data = [d for d in data]
    data = data[1]
    data = data.encode('utf-8').decode('unicode-escape')
    data = data.split('=="],[[')
    data = [d.replace(']', '').replace('[', '').replace(',null', '').split(',') for d in data]
    return data

def process_reviews(content: list, company_name: str) -> Review:
    """

    :param content:
    :param company_name:
    :return:
    """
    """
     after processing multiple files, I found that there are multiple ways to find the information, which I needed.
      i) The reviewer name is always at 1st index.
      ii) The review time is at 4th index.
      iii) The review content starts at 5th index, and it can continue until the next index is not starting with space
        or /n tag.
      iv) The review rating is always at the next index of review content ending index.
      v) The reply from owner is always at the 2nd next index of '"Als unangemessen melden"', So if we have that index
        starting with '"vor' which denotes it's the reply time information, then we mark the reply True else False
      vi) The actual reply from the owner is always at the next index of the reply time stamp, and it follows the same
        approach of using multiple index, so we can continue until the next index is not starting with space or /n tag.
      vii) The review link is always starts with 'https://www.google.com/maps/reviews/data='.
      
      Note: This defined order is only feasible with data processing, which I have done.
    """
    review_text = ''
    reviewer_name = content[1]
    review_time_information = content[4]
    index = 5
    while True:
        review_text += content[index]
        index += 1
        if not (content[index].startswith(' ') or content[index].startswith('\n')):
            break
    rating = content[index]
    index = content.index('"Als unangemessen melden"')
    index += 2
    reply = True if content[index].startswith('"vor') else False
    reply_content = ''
    if reply:
        index += 1
        while True:
            reply_content += content[index]
            index += 1
            if not (content[index].startswith(' ') or content[index].startswith('\n')):
                break
    reply_content = reply_content if reply else ''
    review_link = [a for a in content if 'https://www.google.com/maps/reviews/data=' in a]
    review_link = review_link[0] if review_link else None
    review = Review(
        company_name,
        reviewer_name, review_time_information,
        review_text,rating,
        reply, reply_content, review_link
    )
    return review

def read_file(file_path: str)-> str:
    """

    :param file_path:
    :return:
    """
    with open(file_path, 'r') as f:
        data = f.read()
    return data

def get_files(filepath: str) -> list:
    """
    :param filepath: str
    :return: list[str]
    """
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.txt'))
        for f in files:
            all_files.append(os.path.abspath(f))

    return all_files