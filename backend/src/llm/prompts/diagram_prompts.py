"""
Specialized prompt templates for different diagram types.
Each prompt is tailored to generate high-quality, specific diagram types.
"""

# Component Diagram Prompt
COMPONENT_DIAGRAM_PROMPT = """You are an expert software architect specializing in component diagrams.

Generate a Mermaid component diagram (graph TD syntax) based on the provided codebase context.

CONTEXT:
- Project Type: {project_type}
- Total Components: {total_components}
- External Dependencies: {external_dependencies}
- Frameworks: {frameworks}

COMPONENTS:
{components}

RELATIONSHIPS:
{component_relationships}

REQUIREMENTS:
1. Show all major components/modules with clear boundaries
2. Display external dependencies (databases, APIs, frameworks) as separate nodes
3. Use meaningful labels for relationships (uses, depends on, communicates with)
4. Group related components visually if possible
5. Keep the diagram clean and readable (max 15 nodes)
6. Use subgraphs for logical grouping where appropriate

MERMAID SYNTAX:
- Use `graph TD` for top-down layout
- Components: `ComponentName[Component Name]`
- External systems: `ExtSystem{{External System}}`
- Relationships: `A --> B` with optional labels `A -->|uses| B`
- Subgraphs: `subgraph Title ... end`

Generate ONLY the Mermaid code, no explanation. Start with `graph TD`.
"""

# Class Diagram Prompt
CLASS_DIAGRAM_PROMPT = """You are an expert in object-oriented design and UML class diagrams.

Generate a Mermaid class diagram based on the provided class information.

CONTEXT:
- Total Classes: {total_classes}
- Has Inheritance: {has_inheritance}
- Has Composition: {has_composition}

CLASSES:
{classes}

RELATIONSHIPS:
{relationships}

REQUIREMENTS:
1. Show all classes with their key attributes and methods
2. Display proper visibility modifiers (+ public, - private, # protected)
3. Show inheritance relationships with solid arrows
4. Show composition/aggregation with appropriate arrows
5. Show associations and dependencies with dashed arrows
6. Keep method/attribute lists concise (max 5-8 per class)
7. Focus on the most important classes if there are many

MERMAID SYNTAX:
- Start with `classDiagram`
- Class definition:
  ```
  class ClassName {{
    +publicAttribute: type
    -privateAttribute: type
    +publicMethod()
    -privateMethod()
  }}
  ```
- Inheritance: `Parent <|-- Child`
- Composition: `ClassA *-- ClassB`
- Aggregation: `ClassA o-- ClassB`
- Association: `ClassA --> ClassB`
- Dependency: `ClassA ..> ClassB`

Generate ONLY the Mermaid code, no explanation. Start with `classDiagram`.
"""

# Sequence Diagram Prompt
SEQUENCE_DIAGRAM_PROMPT = """You are an expert in documenting system interactions and message flows.

Generate a Mermaid sequence diagram for the following scenario.

SCENARIO: {scenario}

CONTEXT:
- Entry Point: {entry_point}
- Total Interactions: {interaction_count}

PARTICIPANTS:
{participants}

EXECUTION FLOW:
{execution_flow}

REQUIREMENTS:
1. Show all participants (actors, systems, components)
2. Display message flows in chronological order
3. Use appropriate arrow types (synchronous, asynchronous, return)
4. Include activation boxes for active processing
5. Add notes for important decisions or conditions
6. Keep the flow focused on the main scenario (max 12-15 interactions)
7. Use alt/opt/loop blocks for conditional/iterative logic if present

MERMAID SYNTAX:
- Start with `sequenceDiagram`
- Participants: `participant Name` or `actor Name`
- Messages: `A->>B: message` (sync), `A-->>B: response` (async)
- Activation: `activate A` / `deactivate A`
- Notes: `Note right of A: text` or `Note over A,B: text`
- Conditional: `alt Condition ... else ... end`
- Loop: `loop Times ... end`

Generate ONLY the Mermaid code, no explanation. Start with `sequenceDiagram`.
"""

# Activity Diagram Prompt
ACTIVITY_DIAGRAM_PROMPT = """You are an expert in business process modeling and workflow documentation.

Generate a Mermaid flowchart representing the activity flow.

SCENARIO: {scenario}

CONTEXT:
- Total Activities: {total_activities}

KEY ACTIVITIES:
{activities}

CONTROL FLOW:
{control_flow}

DECISION POINTS:
{decision_points}

REQUIREMENTS:
1. Show the workflow from start to end with clear flow direction
2. Display decision points (conditionals) with diamond shapes
3. Show parallel activities if they exist
4. Include start/end nodes
5. Use descriptive labels for each activity
6. Keep the flow readable (max 15-20 nodes)
7. Group related activities visually if possible

MERMAID SYNTAX:
- Start with `flowchart TD` (top-down) or `flowchart LR` (left-right)
- Start/End: `start([Start])`, `stop([End])`
- Activity: `activity[Activity Name]`
- Decision: `decision{{Decision?}}`
- Process flow: `A --> B` with optional labels `A -->|yes| B`
- Subgraphs for grouping: `subgraph Title ... end`

Generate ONLY the Mermaid code, no explanation. Start with `flowchart TD`.
"""

# Data Flow Diagram Prompt
DATA_FLOW_DIAGRAM_PROMPT = """You are an expert in data architecture and information flow modeling.

Generate a Mermaid flowchart showing data flow through the system.

CONTEXT:
- Has Database: {has_database}
- Has API: {has_api}

DATA SOURCES:
{data_sources}

DATA TRANSFORMATIONS:
{transformations}

DATA SINKS:
{data_sinks}

DATA FLOWS:
{data_flows}

REQUIREMENTS:
1. Show data sources (inputs) on the left
2. Show data transformations/processes in the middle
3. Show data sinks (outputs, storage) on the right
4. Use clear labels for data being passed
5. Highlight important transformations
6. Show data stores (databases, caches) with special styling
7. Keep the diagram focused (max 12-15 nodes)

MERMAID SYNTAX:
- Start with `flowchart LR` (left-to-right for data flow)
- External entity: `entity([External Entity])`
- Process: `process[Process Name]`
- Data store: `database[(Database)]` or `cache[/Cache\\]`
- Data flow: `A -->|data_name| B`
- Parallel flows: use multiple arrows

Generate ONLY the Mermaid code, no explanation. Start with `flowchart LR`.
"""

# C4 Context Diagram Prompt
C4_CONTEXT_DIAGRAM_PROMPT = """You are an expert in C4 architecture modeling and system context documentation.

Generate a Mermaid C4 Context diagram showing the system in its environment.

CONTEXT:
- System Name: {system_name}
- Project Type: {project_type}

USERS/ACTORS:
{users}

EXTERNAL SYSTEMS:
{external_systems}

INTERACTIONS:
{interactions}

REQUIREMENTS:
1. Place the main system in the center
2. Show all users/actors that interact with the system
3. Show all external systems the system depends on
4. Use clear, descriptive relationship labels
5. Follow C4 model conventions (Person, System, relationship)
6. Keep the diagram clean (max 8-10 external entities)

MERMAID SYNTAX:
- Note: Use Mermaid flowchart syntax for C4 context modeling
- Start with `flowchart TD`
- Person/Actor: `user([User Name])`
- System (main): `system[System Name]`
- External System: `ext{{External System}}`
- Relationships: `user -->|uses| system`, `system -->|reads/writes| ext`
- Style with subgraphs if needed

Generate ONLY the Mermaid code, no explanation. Start with `flowchart TD`.
"""

# ER Diagram Prompt
ER_DIAGRAM_PROMPT = """You are an expert in database design and entity-relationship modeling.

Generate a Mermaid ER diagram showing the database schema.

CONTEXT:
- Total Entities: {total_entities}

ENTITIES:
{entities}

RELATIONSHIPS:
{relationships}

REQUIREMENTS:
1. Show all entities (tables) with their attributes
2. Mark primary keys clearly
3. Show relationships with proper cardinality (1:1, 1:N, N:M)
4. Include foreign key relationships
5. Use clear entity and attribute names
6. Keep attribute lists concise (max 8 per entity)

MERMAID SYNTAX:
- Start with `erDiagram`
- Entity with attributes:
  ```
  ENTITY_NAME {{
    int id PK
    string name
    datetime created_at
  }}
  ```
- Relationships:
  - One-to-one: `A ||--|| B : relationship`
  - One-to-many: `A ||--o{{ B : relationship`
  - Many-to-many: `A }}--{{ B : relationship`

Generate ONLY the Mermaid code, no explanation. Start with `erDiagram`.
"""

# Package Diagram Prompt (similar to component but more detailed)
PACKAGE_DIAGRAM_PROMPT = """You are an expert in software architecture and package organization.

Generate a Mermaid graph showing package structure and dependencies.

CONTEXT:
- Project Type: {project_type}
- Total Components: {total_components}

COMPONENTS:
{components}

RELATIONSHIPS:
{component_relationships}

REQUIREMENTS:
1. Show package hierarchy using nested subgraphs
2. Display inter-package dependencies clearly
3. Group related packages together
4. Show external dependencies separately
5. Use consistent naming conventions
6. Keep the structure readable (max 20 packages)

MERMAID SYNTAX:
- Start with `graph TD`
- Packages as subgraphs:
  ```
  subgraph package_name
    A[Module A]
    B[Module B]
  end
  ```
- Dependencies: `A --> B` with labels
- External: `ext{{External Package}}`

Generate ONLY the Mermaid code, no explanation. Start with `graph TD`.
"""

# State Machine Diagram Prompt
STATE_DIAGRAM_PROMPT = """You are an expert in state machine modeling and behavioral documentation.

Generate a Mermaid state diagram showing state transitions.

SCENARIO: {scenario}

CONTEXT:
- Total Activities: {total_activities}

ACTIVITIES:
{activities}

CONTROL FLOW:
{control_flow}

REQUIREMENTS:
1. Show all possible states the system can be in
2. Display state transitions with clear trigger labels
3. Mark initial and final states
4. Include composite states if appropriate
5. Show transition conditions/guards
6. Keep the diagram focused (max 10-12 states)

MERMAID SYNTAX:
- Start with `stateDiagram-v2`
- States: simple state names or `state "State Name" as alias`
- Transitions: `State1 --> State2 : trigger/event`
- Initial: `[*] --> State1`
- Final: `State --> [*]`
- Composite: `state CompositeState { ... }`

Generate ONLY the Mermaid code, no explanation. Start with `stateDiagram-v2`.
"""

# Deployment Diagram Prompt (using C4 approach)
DEPLOYMENT_DIAGRAM_PROMPT = """You are an expert in infrastructure architecture and deployment modeling.

Generate a Mermaid diagram showing deployment architecture.

CONTEXT:
- Project Type: {project_type}
- External Systems: {external_systems}

REQUIREMENTS:
1. Show deployment nodes (servers, containers, cloud services)
2. Display deployed components/artifacts
3. Show network connections and protocols
4. Include infrastructure services (databases, caches, queues)
5. Use appropriate icons/shapes for different node types
6. Keep the diagram clear (max 12 nodes)

MERMAID SYNTAX:
- Start with `flowchart TD`
- Server/Container: `server[Server Name]`
- Cloud service: `cloud{{Cloud Service}}`
- Database: `db[(Database)]`
- Connections: `A -->|HTTP/HTTPS| B`, `A -->|TCP| B`
- Group by environment: use subgraphs

Generate ONLY the Mermaid code, no explanation. Start with `flowchart TD`.
"""

# Prompt template mapping
PROMPT_TEMPLATES = {
    'component': COMPONENT_DIAGRAM_PROMPT,
    'class': CLASS_DIAGRAM_PROMPT,
    'sequence': SEQUENCE_DIAGRAM_PROMPT,
    'activity': ACTIVITY_DIAGRAM_PROMPT,
    'data_flow': DATA_FLOW_DIAGRAM_PROMPT,
    'c4_context': C4_CONTEXT_DIAGRAM_PROMPT,
    'c4_container': C4_CONTEXT_DIAGRAM_PROMPT,  # Reuse with modifications
    'er_diagram': ER_DIAGRAM_PROMPT,
    'package': PACKAGE_DIAGRAM_PROMPT,
    'state': STATE_DIAGRAM_PROMPT,
    'deployment': DEPLOYMENT_DIAGRAM_PROMPT
}


def get_prompt_for_diagram(diagram_type: str, context: dict) -> str:
    """
    Get formatted prompt for specific diagram type.
    
    Args:
        diagram_type: Type of diagram to generate
        context: Extracted context from ContextExtractor
        
    Returns:
        Formatted prompt string ready for LLM
    """
    template = PROMPT_TEMPLATES.get(diagram_type, COMPONENT_DIAGRAM_PROMPT)
    
    # Format context values for prompt
    formatted_context = _format_context_for_prompt(context)
    
    try:
        return template.format(**formatted_context)
    except KeyError as e:
        # Fallback: provide default values for missing keys
        print(f"Warning: Missing key {e} in context for {diagram_type}")
        return template.format(**{**_get_default_context(), **formatted_context})


def _format_context_for_prompt(context: dict) -> dict:
    """Format context dictionary for prompt template."""
    formatted = {}
    
    for key, value in context.items():
        if isinstance(value, list):
            if len(value) > 0 and isinstance(value[0], dict):
                # Format list of dicts as bullet points
                formatted[key] = '\n'.join([f"- {_format_dict(item)}" for item in value])
            else:
                # Format simple list
                formatted[key] = '\n'.join([f"- {item}" for item in value]) if value else "None"
        elif isinstance(value, dict):
            formatted[key] = _format_dict(value)
        elif isinstance(value, bool):
            formatted[key] = "Yes" if value else "No"
        else:
            formatted[key] = str(value)
    
    return formatted


def _format_dict(d: dict) -> str:
    """Format dictionary as readable string."""
    parts = []
    for k, v in d.items():
        if isinstance(v, list):
            v = f"[{len(v)} items]"
        elif isinstance(v, dict):
            v = "{...}"
        parts.append(f"{k}: {v}")
    return ", ".join(parts)


def _get_default_context() -> dict:
    """Get default context values."""
    return {
        'project_type': 'unknown',
        'total_components': 0,
        'external_dependencies': 'None',
        'frameworks': 'None',
        'components': 'No components detected',
        'component_relationships': 'No relationships',
        'total_classes': 0,
        'has_inheritance': 'No',
        'has_composition': 'No',
        'classes': 'No classes detected',
        'relationships': 'No relationships',
        'scenario': 'System workflow',
        'entry_point': 'main',
        'interaction_count': 0,
        'participants': 'System',
        'execution_flow': 'No flow detected',
        'total_activities': 0,
        'activities': 'No activities',
        'control_flow': 'No flow',
        'decision_points': 'No decisions',
        'has_database': 'No',
        'has_api': 'No',
        'data_sources': 'Unknown',
        'transformations': 'None',
        'data_sinks': 'Unknown',
        'data_flows': 'No flows',
        'system_name': 'System',
        'users': 'User',
        'external_systems': 'None',
        'interactions': 'No interactions',
        'total_entities': 0,
        'entities': 'No entities',
    }
