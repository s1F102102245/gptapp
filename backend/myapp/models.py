from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)  # タスクのタイトル
    description = models.TextField(blank=True)  # タスクの説明（オプショナル）
    created_at = models.DateTimeField(auto_now_add=True)  # タスクの作成日時
    due_date = models.DateTimeField(null=True, blank=True)  # タスクの期限（オプショナル）

    def __str__(self):
        return self.title