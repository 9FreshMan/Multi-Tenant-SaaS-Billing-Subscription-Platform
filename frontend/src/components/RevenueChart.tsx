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
} from 'recharts';
import { format } from 'date-fns';

interface RevenueDataPoint {
    date: string;
    revenue: number;
    subscriptions: number;
}

interface RevenueChartProps {
    data?: RevenueDataPoint[];
    type?: 'line' | 'area' | 'bar';
    height?: number;
}

const RevenueChart: React.FC<RevenueChartProps> = ({
    data = generateMockData(),
    type = 'area',
    height = 300,
}) => {
    const formatCurrency = (value: number) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0,
        }).format(value);
    };

    const formatDate = (dateStr: string) => {
        try {
            return format(new Date(dateStr), 'MMM dd');
        } catch {
            return dateStr;
        }
    };

    const CustomTooltip = ({ active, payload }: any) => {
        if (active && payload && payload.length) {
            return (
                <div className="bg-white p-4 rounded-lg shadow-lg border border-gray-200">
                    <p className="text-sm font-medium text-gray-900">
                        {formatDate(payload[0].payload.date)}
                    </p>
                    <p className="text-sm text-blue-600 mt-1">
                        Revenue: {formatCurrency(payload[0].value)}
                    </p>
                    {payload[1] && (
                        <p className="text-sm text-green-600">
                            Subscriptions: {payload[1].value}
                        </p>
                    )}
                </div>
            );
        }
        return null;
    };

    const renderChart = () => {
        const commonProps = {
            data,
            margin: { top: 10, right: 30, left: 0, bottom: 0 },
        };

        switch (type) {
            case 'line':
                return (
                    <LineChart {...commonProps}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                        <XAxis
                            dataKey="date"
                            tickFormatter={formatDate}
                            stroke="#9ca3af"
                            fontSize={12}
                        />
                        <YAxis
                            tickFormatter={formatCurrency}
                            stroke="#9ca3af"
                            fontSize={12}
                        />
                        <Tooltip content={<CustomTooltip />} />
                        <Legend />
                        <Line
                            type="monotone"
                            dataKey="revenue"
                            stroke="#3b82f6"
                            strokeWidth={2}
                            dot={{ fill: '#3b82f6', r: 4 }}
                            activeDot={{ r: 6 }}
                            name="Revenue"
                        />
                        <Line
                            type="monotone"
                            dataKey="subscriptions"
                            stroke="#10b981"
                            strokeWidth={2}
                            dot={{ fill: '#10b981', r: 4 }}
                            name="Subscriptions"
                        />
                    </LineChart>
                );

            case 'area':
                return (
                    <AreaChart {...commonProps}>
                        <defs>
                            <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                            </linearGradient>
                            <linearGradient id="colorSubs" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
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
                            tickFormatter={formatCurrency}
                            stroke="#9ca3af"
                            fontSize={12}
                        />
                        <Tooltip content={<CustomTooltip />} />
                        <Legend />
                        <Area
                            type="monotone"
                            dataKey="revenue"
                            stroke="#3b82f6"
                            strokeWidth={2}
                            fillOpacity={1}
                            fill="url(#colorRevenue)"
                            name="Revenue"
                        />
                        <Area
                            type="monotone"
                            dataKey="subscriptions"
                            stroke="#10b981"
                            strokeWidth={2}
                            fillOpacity={1}
                            fill="url(#colorSubs)"
                            name="Subscriptions"
                        />
                    </AreaChart>
                );

            case 'bar':
                return (
                    <BarChart {...commonProps}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                        <XAxis
                            dataKey="date"
                            tickFormatter={formatDate}
                            stroke="#9ca3af"
                            fontSize={12}
                        />
                        <YAxis
                            tickFormatter={formatCurrency}
                            stroke="#9ca3af"
                            fontSize={12}
                        />
                        <Tooltip content={<CustomTooltip />} />
                        <Legend />
                        <Bar dataKey="revenue" fill="#3b82f6" name="Revenue" radius={[8, 8, 0, 0]} />
                        <Bar dataKey="subscriptions" fill="#10b981" name="Subscriptions" radius={[8, 8, 0, 0]} />
                    </BarChart>
                );

            default:
                return <></>;
        }
    };

    return (
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Revenue & Growth</h3>
                <p className="text-sm text-gray-500">Last 30 days overview</p>
            </div>
            <ResponsiveContainer width="100%" height={height}>
                {renderChart()}
            </ResponsiveContainer>
        </div>
    );
};

// Mock data generator for demo purposes
function generateMockData(): RevenueDataPoint[] {
    const data: RevenueDataPoint[] = [];
    const today = new Date();

    for (let i = 29; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);

        // Generate realistic growth pattern
        const baseRevenue = 5000;
        const growth = (29 - i) * 150;
        const randomVariation = Math.random() * 1000 - 500;
        const revenue = Math.max(0, baseRevenue + growth + randomVariation);

        const baseSubs = 50;
        const subGrowth = Math.floor((29 - i) * 2);
        const subVariation = Math.floor(Math.random() * 5 - 2);
        const subscriptions = Math.max(0, baseSubs + subGrowth + subVariation);

        data.push({
            date: date.toISOString().split('T')[0],
            revenue: Math.round(revenue),
            subscriptions,
        });
    }

    return data;
}

export default RevenueChart;
