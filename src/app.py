from flask import Flask, render_template, request, redirect, url_for, flash
from varasto import Varasto

app = Flask(__name__)
app.secret_key = 'dev_secret_key_change_in_production'

# In-memory storage for warehouses
warehouses = {}
warehouse_id_counter = 0


@app.route('/')
def index():
    """Display all warehouses."""
    return render_template('index.html', warehouses=warehouses)


@app.route('/warehouse/create', methods=['GET', 'POST'])
def create_warehouse():
    """Create a new warehouse."""
    if request.method == 'POST':
        global warehouse_id_counter
        name = request.form.get('name', '').strip()
        try:
            tilavuus = float(request.form.get('tilavuus', 0))
            alku_saldo = float(request.form.get('alku_saldo', 0))
            
            if not name:
                flash('Warehouse name is required', 'error')
                return render_template('create_warehouse.html')
            
            if tilavuus <= 0:
                flash('Capacity must be greater than 0', 'error')
                return render_template('create_warehouse.html')
            
            if alku_saldo < 0:
                flash('Initial balance cannot be negative', 'error')
                return render_template('create_warehouse.html')
            
            warehouse_id_counter += 1
            warehouses[warehouse_id_counter] = {
                'id': warehouse_id_counter,
                'name': name,
                'varasto': Varasto(tilavuus, alku_saldo)
            }
            flash(f'Warehouse "{name}" created successfully', 'success')
            return redirect(url_for('index'))
        except ValueError:
            flash('Invalid number format', 'error')
            return render_template('create_warehouse.html')
    
    return render_template('create_warehouse.html')


@app.route('/warehouse/<int:warehouse_id>')
def view_warehouse(warehouse_id):
    """View warehouse details."""
    if warehouse_id not in warehouses:
        flash('Warehouse not found', 'error')
        return redirect(url_for('index'))
    
    warehouse = warehouses[warehouse_id]
    return render_template('view_warehouse.html', warehouse=warehouse)


@app.route('/warehouse/<int:warehouse_id>/edit', methods=['GET', 'POST'])
def edit_warehouse(warehouse_id):
    """Edit warehouse details."""
    if warehouse_id not in warehouses:
        flash('Warehouse not found', 'error')
        return redirect(url_for('index'))
    
    warehouse = warehouses[warehouse_id]
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        try:
            tilavuus = float(request.form.get('tilavuus', 0))
            
            if not name:
                flash('Warehouse name is required', 'error')
                return render_template('edit_warehouse.html', warehouse=warehouse)
            
            if tilavuus <= 0:
                flash('Capacity must be greater than 0', 'error')
                return render_template('edit_warehouse.html', warehouse=warehouse)
            
            # Keep the current saldo but update capacity
            current_saldo = warehouse['varasto'].saldo
            warehouse['name'] = name
            warehouse['varasto'] = Varasto(tilavuus, current_saldo)
            
            flash(f'Warehouse "{name}" updated successfully', 'success')
            return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))
        except ValueError:
            flash('Invalid number format', 'error')
            return render_template('edit_warehouse.html', warehouse=warehouse)
    
    return render_template('edit_warehouse.html', warehouse=warehouse)


@app.route('/warehouse/<int:warehouse_id>/delete', methods=['POST'])
def delete_warehouse(warehouse_id):
    """Delete a warehouse."""
    if warehouse_id in warehouses:
        name = warehouses[warehouse_id]['name']
        del warehouses[warehouse_id]
        flash(f'Warehouse "{name}" deleted successfully', 'success')
    else:
        flash('Warehouse not found', 'error')
    
    return redirect(url_for('index'))


@app.route('/warehouse/<int:warehouse_id>/add', methods=['POST'])
def add_to_warehouse(warehouse_id):
    """Add content to warehouse."""
    if warehouse_id not in warehouses:
        flash('Warehouse not found', 'error')
        return redirect(url_for('index'))
    
    warehouse = warehouses[warehouse_id]
    try:
        maara = float(request.form.get('maara', 0))
        
        if maara <= 0:
            flash('Amount must be greater than 0', 'error')
            return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))
        
        available_space = warehouse['varasto'].paljonko_mahtuu()
        if maara > available_space:
            flash(f'Not enough space. Available: {available_space:.2f}', 'error')
            return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))
        
        warehouse['varasto'].lisaa_varastoon(maara)
        flash(f'Added {maara:.2f} to warehouse', 'success')
    except ValueError:
        flash('Invalid number format', 'error')
    
    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


@app.route('/warehouse/<int:warehouse_id>/remove', methods=['POST'])
def remove_from_warehouse(warehouse_id):
    """Remove content from warehouse."""
    if warehouse_id not in warehouses:
        flash('Warehouse not found', 'error')
        return redirect(url_for('index'))
    
    warehouse = warehouses[warehouse_id]
    try:
        maara = float(request.form.get('maara', 0))
        
        if maara <= 0:
            flash('Amount must be greater than 0', 'error')
            return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))
        
        if maara > warehouse['varasto'].saldo:
            flash(f'Not enough content. Available: {warehouse["varasto"].saldo:.2f}', 'error')
            return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))
        
        warehouse['varasto'].ota_varastosta(maara)
        flash(f'Removed {maara:.2f} from warehouse', 'success')
    except ValueError:
        flash('Invalid number format', 'error')
    
    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


if __name__ == '__main__':
    app.run(debug=True)
