import React from 'react';

interface KanbanCardProps {
    title: string;
    progress: number;
    status: string;
    color: string;
}

const KanbanCard: React.FC<KanbanCardProps> = ({ title, progress, status, color }) => (
    <div className={`neo-card ${color} mb-4 cursor-grab active:cursor-grabbing`}>
        <h4 className="font-bold truncate">{title}</h4>
        <div className="mt-2 bg-neo-black h-4 border-2 border-neo-black overflow-hidden">
            <div
                className="bg-neo-white h-full transition-all duration-500"
                style={{ width: `${progress}%` }}
            />
        </div>
        <div className="mt-2 flex justify-between items-center text-xs font-mono uppercase">
            <span>{status}</span>
            <span>{progress}%</span>
        </div>
    </div>
);

const KanbanBoard: React.FC = () => {
    const columns = [
        { title: 'Queued', color: 'bg-neo-gray', tasks: [{ title: 'Quantum Computing', progress: 0, status: 'WAITING' }] },
        { title: 'Processing', color: 'bg-neo-yellow', tasks: [{ title: 'Vegan Cooking', progress: 45, status: 'DRAFTING' }] },
        { title: 'Review', color: 'bg-neo-pink', tasks: [{ title: 'Modern History', progress: 85, status: 'CRITIC_PASS' }] },
        { title: 'Done', color: 'bg-neo-cyan', tasks: [{ title: 'AI Ethics', progress: 100, status: 'SYNCED' }] },
    ];

    return (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 p-6">
            {columns.map((col) => (
                <div key={col.title} className="flex flex-col gap-4">
                    <h3 className="neo-card bg-neo-black text-neo-white text-center py-2 text-xl italic uppercase">
                        {col.title}
                    </h3>
                    <div className="flex-1 min-h-[400px]">
                        {col.tasks.map((task, i) => (
                            <KanbanCard key={i} {...task} color={col.color} />
                        ))}
                    </div>
                </div>
            ))}
        </div>
    );
};

export default KanbanBoard;
