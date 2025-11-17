import React from 'react';
import {
    LineChart,
    Line,
    AreaChart,
    Area,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
    PieChart,
    Pie,
    Cell,
} from 'recharts';
import { format, subDays } from 'date-fns';

interface UsageDataPoint {
    date: string;
    apiCalls: number;
    storage: number;
    bandwidth: number;
}

interface UsageChartProps {
    data?: UsageDataPoint[];
    metric?: 'apiCalls' | 'storage' | 'bandwidth' | 'all';
    height?: number;
}

const UsageChart: React.FC<UsageChartProps> = ({
    data = generateMockUsageData(),
    metric = 'all',
    height = 300,
}) => {
    const formatDate = (dateStr: string) => {
        try {
            return format(new Date(dateStr), 'MMM dd');
        } catch {
            return dateStr;
        }
    };

    const formatNumber = (value: number) => {
        if (value >= 1000) {
            return `${(value / 1000).toFixed(1)}k`;
        }
        return value.toString();
    };

    const formatStorage = (value: number) => {
        return `${(value / 1024).toFixed(1)} GB`;
    };

    const CustomTooltip = ({ active, payload, label }: any) => {
        if (active && payload && payload.length) {
            return (
                <div className="bg-white p-3 rounded-lg shadow-lg border border-gray-200">
                    <p className="text-sm font-medium text-gray-900 mb-2">
                        {formatDate(label)}
                    </p>
                    {payload.map((entry: any, index: number) => (
                        <p key={index} className="text-sm" style={{ color: entry.color }}>
                            {entry.name}: {entry.name === 'Storage'
                                ? formatStorage(entry.value)
                                : formatNumber(entry.value)}
                        </p>
                    ))}
                </div>
            );
        }
        return null;
    };

    if (metric === 'all') {
        return (
            <div className="space-y-6">
                {/* API Calls Chart */}
                <div className="bg-white p-4 rounded-lg">
                    <h3 className="text-sm font-semibold text-gray-900 mb-3">API Calls (Last 30 Days)</h3>
                    <ResponsiveContainer width="100%" height={200}>
                        <AreaChart data={data}>
                            <defs>
                                <linearGradient id="colorAPI" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                            <XAxis
                                dataKey="date"
                                tickFormatter={formatDate}
                                stroke="#9ca3af"
                                fontSize={11}
                            />
                            <YAxis
                                tickFormatter={formatNumber}
                                stroke="#9ca3af"
                                fontSize={11}
                            />
                            <Tooltip content={<CustomTooltip />} />
                            <Area
                                type="monotone"
                                dataKey="apiCalls"
                                stroke="#3b82f6"
                                strokeWidth={2}
                                fillOpacity={1}
                                fill="url(#colorAPI)"
                                name="API Calls"
                            />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>

                {/* Combined Storage & Bandwidth */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Storage Chart */}
                    <div className="bg-white p-4 rounded-lg">
                        <h3 className="text-sm font-semibold text-gray-900 mb-3">Storage Usage (MB)</h3>
                        <ResponsiveContainer width="100%" height={180}>
                            <LineChart data={data}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                                <XAxis
                                    dataKey="date"
                                    tickFormatter={formatDate}
                                    stroke="#9ca3af"
                                    fontSize={11}
                                />
                                <YAxis
                                    stroke="#9ca3af"
                                    fontSize={11}
                                />
                                <Tooltip content={<CustomTooltip />} />
                                <Line
                                    type="monotone"
                                    dataKey="storage"
                                    stroke="#10b981"
                                    strokeWidth={2}
                                    dot={{ fill: '#10b981', r: 3 }}
                                    name="Storage"
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>

                    {/* Bandwidth Chart */}
                    <div className="bg-white p-4 rounded-lg">
                        <h3 className="text-sm font-semibold text-gray-900 mb-3">Bandwidth (MB)</h3>
                        <ResponsiveContainer width="100%" height={180}>
                            <BarChart data={data}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                                <XAxis
                                    dataKey="date"
                                    tickFormatter={formatDate}
                                    stroke="#9ca3af"
                                    fontSize={11}
                                />
                                <YAxis
                                    stroke="#9ca3af"
                                    fontSize={11}
                                />
                                <Tooltip content={<CustomTooltip />} />
                                <Bar
                                    dataKey="bandwidth"
                                    fill="#f59e0b"
                                    name="Bandwidth"
                                    radius={[4, 4, 0, 0]}
                                />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>
        );
    }

    // Single metric view
    return (
        <ResponsiveContainer width="100%" height={height}>
            <AreaChart data={data}>
                <defs>
                    <linearGradient id={`color-${metric}`} x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                    </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis
                    dataKey="date"
                    tickFormatter={formatDate}
                    stroke="#9ca3af"
                    fontSize={12}
                />
                <YAxis
                    tickFormatter={metric === 'storage' ? formatStorage : formatNumber}
                    stroke="#9ca3af"
                    fontSize={12}
                />
                <Tooltip content={<CustomTooltip />} />
                <Area
                    type="monotone"
                    dataKey={metric}
                    stroke="#3b82f6"
                    strokeWidth={2}
                    fillOpacity={1}
                    fill={`url(#color-${metric})`}
                    name={metric === 'apiCalls' ? 'API Calls' : metric === 'storage' ? 'Storage' : 'Bandwidth'}
                />
            </AreaChart>
        </ResponsiveContainer>
    );
};

// Resource breakdown pie chart
export const ResourceBreakdownChart: React.FC = () => {
    const data = [
        { name: 'API Calls', value: 1234, color: '#3b82f6' },
        { name: 'Storage', value: 2456, color: '#10b981' },
        { name: 'Bandwidth', value: 15360, color: '#f59e0b' },
        { name: 'Compute', value: 850, color: '#8b5cf6' },
    ];

    const RADIAN = Math.PI / 180;
    const renderCustomizedLabel = ({
        cx,
        cy,
        midAngle,
        innerRadius,
        outerRadius,
        percent,
    }: any) => {
        const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
        const x = cx + radius * Math.cos(-midAngle * RADIAN);
        const y = cy + radius * Math.sin(-midAngle * RADIAN);

        return (
            <text
                x={x}
                y={y}
                fill="white"
                textAnchor={x > cx ? 'start' : 'end'}
                dominantBaseline="central"
                fontSize={12}
                fontWeight="bold"
            >
                {`${(percent * 100).toFixed(0)}%`}
            </text>
        );
    };

    return (
        <div className="bg-white p-4 rounded-lg">
            <h3 className="text-sm font-semibold text-gray-900 mb-3">Resource Distribution</h3>
            <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                    <Pie
                        data={data}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={renderCustomizedLabel}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                    >
                        {data.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                </PieChart>
            </ResponsiveContainer>
        </div>
    );
};

// Mock data generator
function generateMockUsageData(): UsageDataPoint[] {
    const data: UsageDataPoint[] = [];
    const today = new Date();

    for (let i = 29; i >= 0; i--) {
        const date = subDays(today, i);

        // API calls: gradual increase with some variation
        const baseAPI = 30;
        const trend = (29 - i) * 2;
        const apiVariation = Math.random() * 20 - 10;
        const apiCalls = Math.max(0, Math.round(baseAPI + trend + apiVariation));

        // Storage: slowly increasing
        const baseStorage = 2000;
        const storageGrowth = (29 - i) * 15;
        const storage = Math.round(baseStorage + storageGrowth);

        // Bandwidth: varies by weekday
        const dayOfWeek = date.getDay();
        const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;
        const baseBandwidth = isWeekend ? 300 : 600;
        const bandwidthVariation = Math.random() * 200;
        const bandwidth = Math.round(baseBandwidth + bandwidthVariation);

        data.push({
            date: date.toISOString().split('T')[0],
            apiCalls,
            storage,
            bandwidth,
        });
    }

    return data;
}

export default UsageChart;
