'use client';

import ReactFlow, { Background, Controls, MiniMap, addEdge, useEdgesState, useNodesState } from 'reactflow';
import 'reactflow/dist/style.css';
import { useCallback } from 'react';

const initialNodes = [
  { id: 'restaurant', type: 'default', position: { x: 100, y: 100 }, data: { label: 'Restaurant' } },
  { id: 'metric', type: 'default', position: { x: 450, y: 80 }, data: { label: 'Food Cost Metric' } }
];
const initialEdges = [{ id: 'e1', source: 'restaurant', target: 'metric' }];

export function ProcessCanvas() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback((params: any) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

  return (
    <div className="h-[600px] rounded-xl overflow-hidden border border-slate-700">
      <ReactFlow nodes={nodes} edges={edges} onNodesChange={onNodesChange} onEdgesChange={onEdgesChange} onConnect={onConnect} fitView>
        <MiniMap />
        <Controls />
        <Background />
      </ReactFlow>
    </div>
  );
}
