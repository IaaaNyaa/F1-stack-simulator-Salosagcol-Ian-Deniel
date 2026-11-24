"""Flask application for the stack data structure simulator."""
import secrets

from flask import Flask, flash, redirect, render_template, request, session, url_for

from stack_model import Stack

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route('/')
def index():
    stack = Stack(session.get('stack', []))
    popped = list(session.get('popped', []))
    highlight = session.pop('highlight', False)

    return render_template(
        'index.html',
        items=list(reversed(stack.items)),
        size=stack.size(),
        popped=list(reversed(popped)),
        highlight=highlight,
    )


@app.route('/stack', methods=['POST'])
def operate():
    action = request.form.get('action', '').lower()
    value = request.form.get('value', '').strip()
    stack = Stack(session.get('stack', []))
    popped = list(session.get('popped', []))
    highlight = False

    if action == 'push':
        if not value:
            flash('Enter a value before pushing.', 'error')
        elif len(value) > 24:
            flash('Values must be 24 characters or fewer.', 'error')
        elif stack.size() >= 20:
            flash('The stack can hold at most 20 items.', 'error')
        else:
            stack.push(value)
            flash(f'Pushed "{value}" onto the stack.', 'success')
    elif action == 'pop':
        removed = stack.pop()
        if removed is None:
            flash('Cannot pop: the stack is empty.', 'error')
        else:
            popped.append(removed)
            popped = popped[-20:]
            flash(f'Popped "{removed}" from the stack.', 'success')
    elif action == 'peek':
        top = stack.peek()
        if top is None:
            flash('Cannot peek: the stack is empty.', 'error')
        else:
            highlight = True
            flash(f'Top item: "{top}".', 'success')
    elif action == 'clear':
        stack.clear()
        popped.clear()
        flash('Cleared the stack and removed-item history.', 'success')
    else:
        flash('Unknown stack operation.', 'error')

    session['stack'] = stack.items
    session['popped'] = popped
    session['highlight'] = highlight
    return redirect(url_for('index'))


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run()  # Local development only. Stop with Ctrl+C.