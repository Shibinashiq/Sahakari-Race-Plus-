from dashboard.views.imports import *
from dashboard.forms.batchlesson import BatchLessonForm

def batchlesson_delete(request, pk):
    batch_lesson = get_object_or_404(BatchLesson, pk=pk)
    batch_lesson.is_deleted = True
    batch_lesson.save()
    messages.success(request, "Batch lesson deleted successfully!")
    return redirect('dashboard-batch-schedule', pk=batch_lesson.batch.id)




@login_required(login_url='dashboard-login')
def batchlesson_update(request, pk):
    batch_lesson = get_object_or_404(BatchLesson, pk=pk)

    if request.method == 'POST':
        form = BatchLessonForm(request.POST, instance=batch_lesson)
        if form.is_valid():
            form.save()
            messages.success(request, "Batch lesson updated successfully!")
            return redirect('dashboard-batch-schedule', pk=batch_lesson.batch.id)
    else:
        form = BatchLessonForm(instance=batch_lesson)

    context = {
        'form': form,
        'batch_lesson': batch_lesson,
    }
    return render(request, 'ci/template/public/batch/update-batch-lesson.html', context)