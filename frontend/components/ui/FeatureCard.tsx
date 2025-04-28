import {
  PaletteIcon,
  EyeIcon,
  CheckCircleIcon,
  ClockIcon,
  SettingsIcon,
  HelpCircleIcon
} from '@/components/ui/Icons';
import { IconProps } from '@/components/ui/Icons';

type IconName = 'palette' | 'eye' | 'check-circle' | 'clock' | 'settings' | 'help-circle';

interface FeatureCardProps {
  title: string;
  description: string;
  icon: IconName;
}

const iconComponents: Record<IconName, React.ComponentType<IconProps>> = {
  'palette': PaletteIcon,
  'eye': EyeIcon,
  'check-circle': CheckCircleIcon,
  'clock': ClockIcon,
  'settings': SettingsIcon,
  'help-circle': HelpCircleIcon,
};

export function FeatureCard({ title, description, icon }: FeatureCardProps) {
  const IconComponent = iconComponents[icon];

  return (
    <div className="card flex flex-col items-center text-center p-6">
      <div className="bg-primary-50 p-4 rounded-full mb-4">
        <IconComponent className="h-8 w-8 text-primary" />
      </div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}
