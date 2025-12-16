# domains.py
# Domain definitions and metadata for the Perpetual Ideas Machine

DOMAINS = {
    'mechanical-engineering': {
        'name': 'Mechanical Engineering',
        'description': 'Fasteners, joints, mechanisms, and mechanical systems',
        'icon': '⚙️',
        'color': '#3498db'
    },
    'materials-science': {
        'name': 'Materials Science',
        'description': 'Alloys, composites, polymers, and novel materials',
        'icon': '🔬',
        'color': '#9b59b6'
    },
    'chemical-engineering': {
        'name': 'Chemical Engineering',
        'description': 'Synthesis methods, catalysts, and chemical processes',
        'icon': '🧪',
        'color': '#e74c3c'
    },
    'pharmaceutical-chemistry': {
        'name': 'Pharmaceutical Chemistry',
        'description': 'Drug compounds, formulations, and delivery systems',
        'icon': '💊',
        'color': '#1abc9c'
    },
    'electrical-engineering': {
        'name': 'Electrical Engineering',
        'description': 'Circuit designs, power systems, and electronic devices',
        'icon': '⚡',
        'color': '#f39c12'
    },
    'software-algorithms': {
        'name': 'Software Algorithms',
        'description': 'Data structures, optimization methods, and algorithms',
        'icon': '💻',
        'color': '#34495e'
    },
    'biotechnology': {
        'name': 'Biotechnology',
        'description': 'Genetic constructs, protein engineering, and biotech',
        'icon': '🧬',
        'color': '#16a085'
    },
    'environmental-technology': {
        'name': 'Environmental Technology',
        'description': 'Filtration, remediation, recycling, and green tech',
        'icon': '🌱',
        'color': '#27ae60'
    },
    'medical-devices': {
        'name': 'Medical Devices',
        'description': 'Diagnostic tools, surgical instruments, and devices',
        'icon': '🏥',
        'color': '#e67e22'
    },
    'agricultural-technology': {
        'name': 'Agricultural Technology',
        'description': 'Crop systems, pest management, and agtech',
        'icon': '🌾',
        'color': '#d35400'
    }
}


def get_domain_info(domain_key):
    """Get information for a specific domain"""
    return DOMAINS.get(domain_key, {})


def get_all_domains():
    """Get all domains"""
    return DOMAINS

