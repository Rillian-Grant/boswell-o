from django.db import models
import re

import inspect

class Entry(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        tags = self.__scanContentForBaseTags()

        for tag in tags:
            tag = Tag(tag_text=tag, entry=self)
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
        for tag in tags:
            if tag[0] == '#':
                tag = tag[1:]
        return tags

class Tag(models.Model):
    tag_text = models.CharField(max_length=255)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    base = models.BooleanField(default=False)

    def __str__(self): 
        return self.tag_text

    def save(self, *args, **kwargs):
        if self.tag_text in self.entry.getBaseTags():
            self.base = True

        super().save(*args, **kwargs)