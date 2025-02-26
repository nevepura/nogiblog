class PageInfo:
    """
    A class to store information about a webpage.
    """

    def __init__(self, page_link, thumb_link, title, datez):
        """
        Initializes a PageInfo object.

        Args:
            page_link (str): The link to the webpage.
            thumb_link (str): The link to the thumbnail image.
            title (str): The title of the webpage.
            datez (str): The date associated with the webpage (e.g., publication date).
        """
        self.page_link = page_link
        self.thumb_link = thumb_link
        self.title = title
        self.datez = datez

    def __str__(self):
        """
        Returns a string representation of the PageInfo object.
        """
        return f"Title: {self.title}\nPage Link: {self.page_link}\nThumbnail Link: {self.thumb_link}\nDate: {self.datez}"

    def __repr__(self):
        """
        Returns a string representation of the PageInfo object for debugging.
        """
        return f"PageInfo(page_link='{self.page_link}', thumb_link='{self.thumb_link}', title='{self.title}', datez='{self.datez}')"

    def to_dict(self):
        """
        Returns a dictionary representation of the PageInfo object.
        """
        return {
            "page_link": self.page_link,
            "thumb_link": self.thumb_link,
            "title": self.title,
            "datez": self.datez,
        }