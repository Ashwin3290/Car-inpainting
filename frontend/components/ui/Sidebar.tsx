'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import {
  HomeIcon,
  PaletteIcon,
  ClockIcon,
  SettingsIcon,
  HelpCircleIcon
} from '@/components/ui/Icons';

const navigation = [
  { name: 'Home', href: '/', icon: HomeIcon },
  { name: 'Color Studio', href: '/studio', icon: PaletteIcon },
  { name: 'History', href: '/history', icon: ClockIcon },
  { name: 'Settings', href: '/settings', icon: SettingsIcon },
  { name: 'Help', href: '/help', icon: HelpCircleIcon },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="hidden md:flex flex-col w-64 bg-gradient-to-b from-primary to-secondary text-white">
      <div className="px-4 py-6">
        <h1 className="text-xl font-bold">Car Color Studio</h1>
      </div>
      <nav className="flex-1 px-2 py-4 space-y-1">
        {navigation.map((item) => {
          const isActive = pathname === item.href;
          
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex items-center px-4 py-3 text-sm font-medium rounded-md transition-colors",
                {
                  "bg-white/10 text-white": isActive,
                  "text-primary-100 hover:bg-white/5": !isActive,
                }
              )}
            >
              <item.icon className="mr-3 h-5 w-5" />
              {item.name}
            </Link>
          );
        })}
      </nav>
      <div className="px-4 py-6">
        <p className="text-xs text-white/70">
          © 2024 Car Color Studio
          <br />
          Version 1.0.0
        </p>
      </div>
    </div>
  );
}
