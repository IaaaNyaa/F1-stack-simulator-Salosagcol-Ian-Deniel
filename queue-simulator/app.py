"""Flask application for the FIFO queue data structure simulator."""
import secrets

from flask import Flask, flash, redirect, render_template, request, session, url_for

from queue_model import Queue

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route('/')
def index():
    queue = Queue(session.get('queue', []))
    removed = list(session.get('removed', []))
    highlight = session.pop('highlight', False)

    return render_template(
        'index.html',
        items=queue.items,
        size=queue.size(),
        removed=removed,
        highlight=highlight,
    )


@app.route('/queue', methods=['POST'])
def queue_operation():
    action = request.form.get('action', '').lower()
    value = request.form.get('value', '').strip()
    queue = Queue(session.get('queue', []))
    removed = list(session.get('removed', []))
    highlight = False

    if action == 'enqueue':
        if not value:
            flash('Enter a value before enqueueing.', 'error')
        elif len(value) > 24:
            flash('Values must be 24 characters or fewer.', 'error')
        elif queue.size() >= 20:
            flash('The queue can hold at most 20 items.', 'error')
        else:
            queue.enqueue(value)
            flash(f'Enqueued "{value}" at the rear of the queue.', 'success')
    elif action == 'dequeue':
        item = queue.dequeue()
        if item is None:
            flash('Cannot dequeue: the queue is empty.', 'error')
        else:
            removed.append(item)
            removed = removed[-20:]
            flash(f'Dequeued "{item}" from the front of the queue.', 'success')
    elif action == 'peek':
        front = queue.peek()
        if front is None:
            flash('Cannot peek: the queue is empty.', 'error')
        else:
            highlight = True
            flash(f'Front item: "{front}".', 'success')
    elif action == 'clear':
        queue.clear()
        removed.clear()
        flash('Cleared the queue and removed-item history.', 'success')
    else:
        flash('Unknown queue operation.', 'error')

    session['queue'] = queue.items
    session['removed'] = removed
    session['highlight'] = highlight
    return redirect(url_for('index'))


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run()  # Local development only. Stop with Ctrl+C.