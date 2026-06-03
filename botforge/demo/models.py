from django.db import models
from .utils import create_chunks
from .gemini_service import generate_embedding

# Create your models here.
class SchoolKnowledge(models.Model):

    title = models.CharField(
        max_length=200
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.title
    
    def save(
        self,
        *args,
        **kwargs
    ):

        super().save(
            *args,
            **kwargs
        )

        self.chunks.all().delete()

        chunks=create_chunks(
            self.content
        )

        chunk_objects=[]

        for chunk in chunks:

            embedding=generate_embedding(
                chunk
            )

            chunk_objects.append(

                SchoolKnowledgeChunk(

                    knowledge=self,

                    chunk_text=chunk,

                    embedding=embedding
                )
            )


        SchoolKnowledgeChunk.objects.bulk_create(
            chunk_objects
        )
    
class SchoolKnowledgeChunk(models.Model):

    knowledge = models.ForeignKey(
        SchoolKnowledge,
        on_delete=models.CASCADE,
        related_name="chunks"
    )

    chunk_text = models.TextField()
    embedding = models.JSONField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"Chunk {self.id}"
    
    
class HealthcareKnowledge(models.Model):

    title = models.CharField(
        max_length=200
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):

        return self.title


    def save(
        self,
        *args,
        **kwargs
    ):

        super().save(
            *args,
            **kwargs
        )


        self.chunks.all().delete()


        chunks = create_chunks(
            self.content
        )


        chunk_objects=[]


        for chunk in chunks:

            embedding=generate_embedding(
                chunk
            )


            chunk_objects.append(

                HealthcareKnowledgeChunk(

                    knowledge=self,

                    chunk_text=chunk,

                    embedding=embedding
                )
            )


        HealthcareKnowledgeChunk.objects.bulk_create(

            chunk_objects
        )


class HealthcareKnowledgeChunk(models.Model):

    knowledge=models.ForeignKey(

        HealthcareKnowledge,

        on_delete=models.CASCADE,

        related_name="chunks"
    )

    chunk_text=models.TextField()

    embedding=models.JSONField(

        null=True,

        blank=True
    )


    created_at=models.DateTimeField(

        auto_now_add=True
    )


    def __str__(self):

        return f"Healthcare Chunk {self.id}"
    
class EcommerceKnowledge(models.Model):

    title=models.CharField(
        max_length=200
    )

    content=models.TextField()

    created_at=models.DateTimeField(
        auto_now_add=True
    )

    updated_at=models.DateTimeField(
        auto_now=True
    )


    def __str__(self):

        return self.title


    def save(
        self,
        *args,
        **kwargs
    ):

        super().save(
            *args,
            **kwargs
        )


        self.chunks.all().delete()


        chunks=create_chunks(
            self.content
        )


        chunk_objects=[]


        for chunk in chunks:

            embedding=generate_embedding(
                chunk
            )


            chunk_objects.append(

                EcommerceKnowledgeChunk(

                    knowledge=self,

                    chunk_text=chunk,

                    embedding=embedding
                )
            )


        EcommerceKnowledgeChunk.objects.bulk_create(

            chunk_objects
        )


class EcommerceKnowledgeChunk(models.Model):

    knowledge=models.ForeignKey(

        EcommerceKnowledge,

        on_delete=models.CASCADE,

        related_name="chunks"
    )


    chunk_text=models.TextField()


    embedding=models.JSONField(

        null=True,

        blank=True
    )


    created_at=models.DateTimeField(

        auto_now_add=True
    )


    def __str__(self):

        return f"Ecommerce Chunk {self.id}"
