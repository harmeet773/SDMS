# Generated by Django 3.1.1 on 2020-10-01 08:59

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import modelcluster.contrib.taggit
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('sdms_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'blog categories',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=models.SET('Delete_tags_to_delete_student_entry'), related_name='tagged_items', to='sdms_app.student')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sdms_app_tags_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='taggedstudent',
            name='content_object',
        ),
        migrations.RemoveField(
            model_name='taggedstudent',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='feesinfo',
            name='fee_submitted',
        ),
        migrations.AddField(
            model_name='feesinfo',
            name='amount',
            field=models.IntegerField(default=0, max_length=6),
        ),
        migrations.AddField(
            model_name='feesinfo',
            name='receipt_given',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='feesinfo',
            name='submission_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Fee submission date'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='feesinfo',
            name='page',
            field=modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submitted_fees', to='sdms_app.student'),
        ),
        migrations.DeleteModel(
            name='StudentTag',
        ),
        migrations.DeleteModel(
            name='TaggedStudent',
        ),
        migrations.AlterField(
            model_name='student',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='sdms_app.Tags', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
