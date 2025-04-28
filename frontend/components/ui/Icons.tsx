import * as FiIcons from 'react-icons/fi';
import React from 'react';

export type IconProps = {
  className?: string;
  'aria-hidden'?: boolean;
  size?: number;
};

export const HomeIcon = (props: IconProps) => <FiIcons.FiHome {...props} />;
export const PaletteIcon = (props: IconProps) => <FiIcons.FiEdit {...props} />;
export const ClockIcon = (props: IconProps) => <FiIcons.FiClock {...props} />;
export const SettingsIcon = (props: IconProps) => <FiIcons.FiSettings {...props} />;
export const HelpCircleIcon = (props: IconProps) => <FiIcons.FiHelpCircle {...props} />;
export const EyeIcon = (props: IconProps) => <FiIcons.FiEye {...props} />;
export const CheckCircleIcon = (props: IconProps) => <FiIcons.FiCheckCircle {...props} />;
export const RefreshCwIcon = (props: IconProps) => <FiIcons.FiRefreshCw {...props} />;
export const TrashIcon = (props: IconProps) => <FiIcons.FiTrash2 {...props} />;
export const DownloadIcon = (props: IconProps) => <FiIcons.FiDownload {...props} />;
export const LoaderIcon = (props: IconProps) => <FiIcons.FiLoader {...props} />;
export const UploadIcon = (props: IconProps) => <FiIcons.FiUpload {...props} />;
