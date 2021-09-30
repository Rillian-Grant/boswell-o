from django.db import models
from django.core.exceptions import ValidationError
import re

import inspect

class Entry(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # TODO: Should be in the view.
    def get_content_with_tag_links(self):
        base_tags = self.tag_set.filter(base=True)
        content = self.content[:] # Copy the string w/o reference
        for tag in base_tags:
            content = re.sub(rf"#({tag.tag_text})\b", f'<a href="?search=%23{tag.tag_text}">#{tag.tag_text}</a>', content, count=1)
        return content


    def save(self, *args, **kwargs):
        # Disallow editing
        if self.pk is not None:
            raise ValidationError("Editing is not allowed")
        
        super().save(*args, **kwargs)
        
        tags = self.__scanContentForBaseTags()

        for tag in tags:
            tag = Tag(tag_text=tag, entry=self, base=True)
            tag.save()
    
    def __str__(self):
        if len(self.content) > 25:
            start = self.content[:22] + "..."
        else:
            start = self.content

        return "Entry {}: {}".format(self.id, start) 
    
    # Should not be used unless you suspect the list of tags is incorrect. Instead use tag_set.filter(base=True)
    def __scanContentForBaseTags(self):
        tags = re.findall("#\w+", self.content)

        # Probably Unnecessary if statement
        for i in range(0, len(tags)):
            if tags[i][0] == '#':
                tags[i] = tags[i][1:]
        return tags

class Tag(models.Model):
    tag_text = models.CharField(max_length=255)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    base = models.BooleanField(default=False)

    class Meta:
        unique_together = ("tag_text", "entry")

    def __str__(self): 
        return "#" + self.tag_text + " on " + str(self.entry.id)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValidationError("Editing tags is not allowed.")

        super().save(*args, **kwargs)